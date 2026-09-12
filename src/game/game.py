import pygame

from src.game.player import Bank, Player
from src.game.board import Board
from src.game.constants import PlayerColors
from src.ui.ui import (
    draw_board,
    draw_player_buttons,
    draw_player_list,
    draw_background,
    get_bottom_height,
    get_top_height,
    draw_button_rects,
    draw_action_bar,
    draw_end_screen,
)


class Game:
    def __init__(self):
        self.bank = Bank()
        self.board = Board()

        self.players = [
            Player("P1", points=0, road_length=0, player_id=1, color=PlayerColors[1]),
            Player("P2", points=0, road_length=0, player_id=2, color=PlayerColors[2]),
            Player("P3", points=0, road_length=0, player_id=3, color=PlayerColors[3]),
            Player("P4", points=0, road_length=0, player_id=4, color=PlayerColors[4]),
        ]

        self.setup_order = [0, 1, 2, 3, 3, 2, 1, 0]
        self.setup_step = 0
        self.setup_action = "settlement"
        self.must_connect_vertex = None
        self.settlements_placed = {1: 0, 2: 0, 3: 0, 4: 0}

        self.current_index = self.setup_order[self.setup_step]
        self.current_player = self.players[self.current_index]
        for p in self.players:
            p.is_turn = False
        self.current_player.is_turn = True

        self.phase = "PLACEMENT"
        self.last_roll = None
        self.last_pick = None
        self.build_mode = None
        self.action_message = ""

        # track largest army
        self.largest_army_owner_id = None
        self.largest_army_size = 0

        self.winner = None
        self.exit_to_menu = False
        self.quit_game = False
        self.win_menu_rect = None
        self.win_quit_rect = None

        self.running = True

    def update_longest_road(self):
        best_player = None
        best_length = 4  # minimum to qualify

        for p in self.players:
            length = self.board.longest_road_length(p.player_id)
            p.road_length = length
            if length > best_length:
                best_length = length
                best_player = p

        if best_player:
            for p in self.players:
                p.has_longest_road = False
            best_player.has_longest_road = True

    def update_largest_army(self, player):
        if player is None:
            return

        try:
            pid = int(player.player_id)
        except Exception:
            return

        try:
            used = int(player.knights_used)
        except Exception:
            used = 0

        if used < 3:
            return

        if self.largest_army_owner_id is None:
            self.largest_army_owner_id = pid
            self.largest_army_size = used
            return

        if pid == self.largest_army_owner_id:
            if used > self.largest_army_size:
                self.largest_army_size = used
            return

        if used > self.largest_army_size:
            self.largest_army_owner_id = pid
            self.largest_army_size = used
            return

    def nearest_point(self, points_dict, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        best_key = None
        best_d2 = None
        for k, (x, y) in points_dict.items():
            delta_x = x - mouse_x
            delta_y = y - mouse_y
            d2 = delta_x * delta_x + delta_y * delta_y
            if best_d2 is None or d2 < best_d2:
                best_d2 = d2
                best_key = k
        return best_key, best_d2

    def handle_event(self, event, screen):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        if self.phase == "WIN":
            if self.win_menu_rect is not None and self.win_menu_rect.collidepoint(event.pos):
                self.exit_to_menu = True
                self.running = False
                return
            if self.win_quit_rect is not None and self.win_quit_rect.collidepoint(event.pos):
                self.quit_game = True
                self.running = False
            return

        if self.phase == "ROBBER":
            if self.last_pick is None:
                return

            tile_centers = self.last_pick.get("tile_centers_by_key", {})
            if not tile_centers:
                return

            scale = float(self.last_pick.get("scale", 1.0))
            threshold = max(24, int(46 * scale))
            thresh2 = threshold * threshold

            tile_key, d2 = self.nearest_point(tile_centers, event.pos)
            if tile_key is None or d2 is None or d2 > thresh2:
                return

            try:
                self.board.robber_tile_key = tile_key
            except Exception:
                pass

            self.phase = "GAME"
            self.action_message = ""
            return

        if self.phase == "PLACEMENT":
            if self.last_pick is None:
                return

            scale = float(self.last_pick.get("scale", 1.0))
            vertex_positions = self.last_pick.get("vertex_positions", {})
            edge_midpoints = self.last_pick.get("edge_midpoints", {})

            threshold = max(14, int(22 * scale))
            thresh2 = threshold * threshold

            try:
                pid = int(self.current_player.player_id or (self.current_index + 1))
            except Exception:
                pid = self.current_index + 1

            if self.setup_action == "settlement":
                vertex, d2 = self.nearest_point(vertex_positions, event.pos)
                if vertex is None or d2 is None or d2 > thresh2:
                    return

                if self.board.add_settlement(vertex, pid):
                    try:
                        self.current_player.structures["settlements"] += 1
                    except Exception:
                        pass

                    self.settlements_placed[pid] += 1

                    # Second settlement grants resources from adjacent tiles.
                    if self.settlements_placed[pid] == 2:
                        gained = self.board.resources_for_settlement(vertex)
                        for r in gained:
                            try:
                                self.current_player.resources[r] += 1
                            except Exception:
                                self.current_player.resources[r] = 1

                    self.must_connect_vertex = vertex
                    self.setup_action = "road"

            elif self.setup_action == "road":
                edge, d2 = self.nearest_point(edge_midpoints, event.pos)
                if edge is None or d2 is None or d2 > thresh2:
                    return

                if self.board.add_road(edge, pid, must_connect_to=self.must_connect_vertex):
                    try:
                        self.current_player.structures["roads"] += 1
                    except Exception:
                        pass

                    self.must_connect_vertex = None
                    self.setup_action = "settlement"
                    self.setup_step += 1

                    if self.setup_step >= len(self.setup_order):
                        self.phase = "GAME"
                        self.current_index = 0
                        for player in self.players:
                            player.is_turn = False
                            player.has_rolled = False
                            player.rolled_value = None
                        self.current_player = self.players[self.current_index]
                        self.current_player.is_turn = True
                    else:
                        self.current_index = self.setup_order[self.setup_step]
                        for player in self.players:
                            player.is_turn = False
                        self.current_player = self.players[self.current_index]
                        self.current_player.is_turn = True

            return

        # get button clicks
        bottom = get_bottom_height(screen)
        rects = draw_button_rects(screen, bottom=bottom)
        action, value = self.current_player.handle_click(rects, event.pos)

        if action == "dice_roll":
            self.last_roll = value
            if value is not None:
                try:
                    rolled = int(value)
                except Exception:
                    rolled = None

                if rolled == 7:
                    self.phase = "ROBBER"
                    self.action_message = "7 rolled: click a tile to move the robber"
                else:
                    self.board.distribute_resources(value, self.players)
            return

        if action == "use_knight":
            try:
                dev_count = int(self.current_player.resources.get("dev", 0))
            except Exception:
                dev_count = 0

            if dev_count <= 0:
                return

            try:
                self.current_player.resources["dev"] = dev_count - 1
            except Exception:
                self.current_player.resources["dev"] = 0

            try:
                self.current_player.knights_used = int(self.current_player.knights_used) + 1
            except Exception:
                self.current_player.knights_used = 1

            self.update_largest_army(self.current_player)

            self.phase = "ROBBER"
            self.action_message = "Knight played: click a tile to move the robber"
            self.build_mode = None
            return

        if action == "select_build":
            # Toggle build mode on/off.
            if self.build_mode == value:
                self.build_mode = None
            else:
                self.build_mode = value
            return

        if action == "end_turn":
            try:
                if not self.current_player.has_rolled:
                    return
            except Exception:
                return

            self.last_roll = None
            self.build_mode = None

            self.current_player.is_turn = False
            self.current_index = (self.current_index + 1) % len(self.players)
            self.current_player = self.players[self.current_index]
            self.current_player.is_turn = True
            # reset game state
            try:
                self.current_player.has_rolled = False
                self.current_player.rolled_value = None
            except Exception:
                pass
            return

        if action == "buy_dev":
            try:
                if not self.current_player.has_rolled:
                    return
            except Exception:
                return

            if self.current_player.buy_item("dev_card"):
                try:
                    self.current_player.resources["dev"] += 1
                except Exception:
                    self.current_player.resources["dev"] = 1
            return

        # build mode
        if self.build_mode is None:
            return
        if self.last_pick is None:
            return
        try:
            if not self.current_player.has_rolled:
                return
        except Exception:
            return

        scale = float(self.last_pick.get("scale", 1.0))
        vertex_positions = self.last_pick.get("vertex_positions", {})
        edge_midpoints = self.last_pick.get("edge_midpoints", {})

        threshold = max(18, int(32 * scale))
        thresh2 = threshold * threshold

        try:
            pid = int(self.current_player.player_id or (self.current_index + 1))
        except Exception:
            pid = self.current_index + 1

        if self.build_mode == "road":
            try:
                current_roads = int(self.current_player.structures.get("roads", 0))
            except Exception:
                current_roads = 0
            if current_roads >= 15:
                return

            edge, d2 = self.nearest_point(edge_midpoints, event.pos)
            if edge is None or d2 is None or d2 > thresh2:
                return

            if not self.current_player.buy_item("road", spend=False):
                return
            if self.board.add_road(edge, pid):
                self.current_player.buy_item("road", spend=True)
                try:
                    self.current_player.structures["roads"] += 1
                except Exception:
                    pass
                self.build_mode = None
            return

        if self.build_mode == "settlement":
            try:
                current_settlements = int(self.current_player.structures.get("settlements", 0))
            except Exception:
                current_settlements = 0
            if current_settlements >= 5:
                return

            vertex, d2 = self.nearest_point(vertex_positions, event.pos)
            if vertex is None or d2 is None or d2 > thresh2:
                return

            if not self.current_player.buy_item("settlement", spend=False):
                return
            if not self.board.can_place_settlement_connected(vertex, pid):
                return
            if self.board.add_settlement(vertex, pid):
                self.current_player.buy_item("settlement", spend=True)
                try:
                    self.current_player.structures["settlements"] += 1
                except Exception:
                    pass
                self.build_mode = None
            return

        if self.build_mode == "city":
            try:
                current_cities = int(self.current_player.structures.get("cities", 0))
            except Exception:
                current_cities = 0
            if current_cities >= 4:
                return

            vertex, d2 = self.nearest_point(vertex_positions, event.pos)
            if vertex is None or d2 is None or d2 > thresh2:
                return

            if not self.current_player.buy_item("city", spend=False):
                return

            if self.board.upgrade_city(vertex, pid):
                self.current_player.buy_item("city", spend=True)
                try:
                    self.current_player.structures["cities"] += 1
                    self.current_player.structures["settlements"] -= 1
                except Exception:
                    pass
                self.build_mode = None
            return

    def draw(self, screen):
        draw_background(screen)

        # get victory points from the board
        for p in self.players:
            try:
                pid = int(p.player_id)
            except Exception:
                continue
            try:
                points = int(self.board.victory_points(pid))
            except Exception:
                points = 0

            bonus = 0
            if self.largest_army_owner_id is not None:
                try:
                    if int(pid) == int(self.largest_army_owner_id) and int(self.largest_army_size) >= 3:
                        bonus = 2
                except Exception:
                    bonus = 0

            try:
                p.points = int(points + bonus)
            except Exception:
                pass

        if self.winner is None:
            for p in self.players:
                try:
                    if int(p.points) >= 10:
                        self.winner = p
                        self.phase = "WIN"
                        self.build_mode = None
                        self.last_roll = None
                        break
                except Exception:
                    pass

        if self.phase == "WIN" and self.winner is not None:
            try:
                winner_name = self.winner.name
            except Exception:
                winner_name = "Player"
            self.win_menu_rect, self.win_quit_rect = draw_end_screen(screen, winner_name)
            return

        top = get_top_height(screen)
        win_message = ""
        if self.phase == "WIN" and self.winner is not None:
            try:
                win_message = f"{self.winner.name} wins!"
            except Exception:
                win_message = "Winner!"

        msg = win_message
        if self.phase == "ROBBER":
            msg = self.action_message

        draw_action_bar(screen, self.current_player, last_roll=self.last_roll, message=msg)
        draw_player_list(screen, self.players, top=top)

        bottom = get_bottom_height(screen)
        self.last_pick = draw_board(screen, self.board, self.current_player, top=top)
        draw_player_buttons(
            screen,
            bottom=bottom,
            last_roll=self.last_roll,
            active_mode=self.build_mode,
            current_player=self.current_player,
        )

