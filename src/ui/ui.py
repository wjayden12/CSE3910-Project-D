from src.ui.utils import get_tile_image, get_card_image
import pygame

from src.game.constants import BLACK, WHITE, BLUE, GRAY, GREEN
from src.game import constants as consts

pygame.font.init()
font = pygame.font.SysFont("trebuchet ms", 20)

tile_files = {
    "brick": "brick_tile.png",
    "grain": "grain_tile.png",
    "wool": "wool_tile.png",
    "lumber": "lumber_tile.png",
    "ore": "ore_tile.png",
    "desert": "desert_tile.png",
}

tile_cache = {}
card_cache = {}
menu_cache = {
    "size": None,
    "surface": None,
}


def get_menu_background(surface):
    surface_width, surface_height = surface.get_size()
    size = (surface_width, surface_height)

    cached_size = menu_cache.get("size")
    cached_surface = menu_cache.get("surface")
    if cached_surface is not None and cached_size == size:
        return cached_surface

    bg = None
    try:
        img = pygame.image.load("sprites/catan_bg.png").convert()
        bg = pygame.transform.scale(img, size)
    except Exception:
        bg = None

    menu_cache["size"] = size
    menu_cache["surface"] = bg
    return bg


def get_top_height(surface):
    return max(44, int(surface.get_height() * 0.06))


# BOARD UI

def draw_board(surface, board, local_player=None, top=0):
    bottom_row = get_bottom_height(surface)
    
    pick = draw_tiles(surface, board, bottom=bottom_row, top=top)
    if pick is not None:
        draw_roads(surface, board, pick)
        draw_settlements(surface, board, pick)
        draw_cities(surface, board, pick)
    draw_exit_button(surface)
    if local_player is not None:
        draw_card_row(surface, local_player)

    return pick


def draw_tiles(surface, board, bottom=0, top=0):
    global tile_cache

    board_rows = board.rows

    screen_width = surface.get_width()
    screen_height = surface.get_height()

    top = int(top)
    bottom = int(bottom)

    available_height = max(1, screen_height - top - bottom)

    tile_height = int(available_height * 0.215 * 0.95)
    tile_width = tile_height
    gap = max(1, tile_width // 40)
    
    max_cols = 0
    for row in board_rows:
        row_length = len(row)
        if row_length > max_cols:
            max_cols = row_length

    x_step = int(tile_width * 0.75) + gap
    y_step = int(tile_height * 0.65) + gap

    board_width = (max_cols - 1) * x_step + tile_width
    board_height = (len(board_rows) - 1) * y_step + tile_height

    start_x = (screen_width - board_width) // 2
    start_y = top + (available_height - board_height) // 2
    start_y = max(top + 10, start_y)

    placements = []
    tile_centers_by_key = {}

    try:
        tile_keys_by_row = board.TILE_KEYS_BY_ROW
    except AttributeError:
        tile_keys_by_row = [
            [0, 1, 2],
            [11, 12, 13, 3],
            [10, 17, 18, 14, 4],
            [9, 16, 15, 5],
            [8, 7, 6],
        ]

    for row_index, row in enumerate(board_rows):
        cols = len(row)
        offset = (max_cols - cols) * x_step // 2

        row_x = start_x + offset
        row_y = start_y + row_index * y_step

        for col_index, tile in enumerate(row):
            x = row_x + col_index * x_step
            y = row_y

            tile_key = tile_keys_by_row[row_index][col_index]
            tile_centers_by_key[tile_key] = (x + tile_width * 0.5, y + tile_height * 0.5)

            placements.append((x, y, tile.resource_type, tile.count))

    # render tiles
    for x, y, resource_type, count in placements:
        cache_key = (resource_type, tile_width, tile_height)
        tile_img = tile_cache.get(cache_key)
        if tile_img is None:
            base_img = get_tile_image(resource_type)
            tile_img = pygame.transform.smoothscale(base_img, (tile_width, tile_height))
            tile_cache[cache_key] = tile_img

        surface.blit(tile_img, (x, y))

        if count is not None:
            font_size = max(14, int(tile_width * 0.18))
            count_font = pygame.font.SysFont("trebuchet ms", font_size, bold=True)

            color = (0, 0, 0)

            cx = x + (tile_width * 0.5)
            cy = y + (tile_height * 0.65)

            txt = count_font.render(str(count), True, color)
            surface.blit(txt, txt.get_rect(center=(int(cx), int(cy))))

    # draw robber
    robber_key = None
    try:
        robber_key = board.robber_tile_key
    except Exception:
        robber_key = None

    if robber_key is not None:
        center = tile_centers_by_key.get(robber_key)
        if center is not None:
            r = max(10, int(tile_width * 0.18))
            cx = int(center[0])
            cy = int(center[1])
            pygame.draw.circle(surface, (170, 170, 170), (cx, cy), r)
            pygame.draw.circle(surface, (0, 0, 0), (cx, cy), r, width=2)

    return calculate_vertex_edges(tile_centers_by_key)


def calculate_vertex_edges(tile_centers_by_key):
    c18 = tile_centers_by_key.get(18)
    c17 = tile_centers_by_key.get(17)
    c12 = tile_centers_by_key.get(12)
    if c18 is None or c17 is None or c12 is None:
        return None

    dx_screen = c18[0] - c17[0]
    dy_screen = c18[1] - c12[1]
    if dx_screen == 0 or dy_screen == 0:
        return None

    base_dx = (consts.TilePositions[18][0] - consts.TilePositions[17][0])
    base_dy = (consts.TilePositions[18][1] - consts.TilePositions[12][1])
    if base_dx == 0 or base_dy == 0:
        return None

    scale_x = dx_screen / base_dx
    scale_y = dy_screen / base_dy

    offset_x = c18[0] - consts.TilePositions[18][0] * scale_x
    offset_y = c18[1] - consts.TilePositions[18][1] * scale_y

    vertex_positions = {}
    for v, pos in consts.SettlementPositions.items():
        vertex_positions[v] = (pos[0] * scale_x + offset_x, pos[1] * scale_y + offset_y)

    edge_midpoints = {}
    for a, b in consts.roads:
        pa = vertex_positions[a]
        pb = vertex_positions[b]
        
        if a < b:
            key = (a, b)
        else:
            key = (b, a)

        mid_x = (pa[0] + pb[0]) / 2.0
        mid_y = (pa[1] + pb[1]) / 2.0

        edge_midpoints[key] = (mid_x, mid_y)

    scale = min(scale_x, scale_y)

    return {
        "scale": scale,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "offset": (offset_x, offset_y),
        "tile_centers_by_key": tile_centers_by_key,
        "vertex_positions": vertex_positions,
        "edge_midpoints": edge_midpoints,
    }


def draw_roads(surface, board, pick):
    vertex_positions = pick["vertex_positions"]
    scale = pick["scale"]

    width = max(4, int(8 * scale))
    for road in board.roads:
        a, b = road.location
        pa = vertex_positions.get(a)
        pb = vertex_positions.get(b)
        if pa is None or pb is None:
            continue

        color = consts.PlayerColors.get(road.owner_id, (0, 0, 0))
        pygame.draw.line(surface, color, (int(pa[0]), int(pa[1])), (int(pb[0]), int(pb[1])), width=width)


def draw_settlements(surface, board, pick):
    vertex_positions = pick["vertex_positions"]
    scale = pick["scale"]

    size = max(10, int(18 * scale))
    half = size // 2

    for settlement in board.settlements:
        p = vertex_positions.get(settlement.location)
        if p is None:
            continue

        color = consts.PlayerColors.get(settlement.owner_id, (0, 0, 0))
        rect = pygame.Rect(int(p[0] - half), int(p[1] - half), size, size)
        pygame.draw.rect(surface, color, rect, border_radius=max(2, size // 6))
        pygame.draw.rect(surface, (255, 255, 255), rect, width=max(2, size // 10), border_radius=max(2, size // 6))


def draw_cities(surface, board, pick):
    vertex_positions = pick["vertex_positions"]
    scale = pick["scale"]

    size = max(14, int(26 * scale))
    half = size // 2

    for city in board.cities:
        p = vertex_positions.get(city.location)
        if p is None:
            continue

        color = consts.PlayerColors.get(city.owner_id, (0, 0, 0))
        rect = pygame.Rect(int(p[0] - half), int(p[1] - half), size, size)
        pygame.draw.rect(surface, color, rect, border_radius=max(2, size // 6))
        pygame.draw.rect(surface, (0, 0, 0), rect, width=max(2, size // 10), border_radius=max(2, size // 6))


def draw_card_row(surface, player):
    global card_cache

    surface_width, surface_height = surface.get_size()
    font = pygame.font.SysFont("trebuchet ms", max(14, int(surface_width * 0.015)))

    cards = [
        ("wood", "lumber"),
        ("brick", "brick"),
        ("sheep", "wool"),
        ("wheat", "grain"),
        ("ore", "ore"),
        ("dev", "dev"),
    ]

    card_width = max(50, int(surface_width * 0.045))
    card_height = int(card_width * 1.35)
    gap = max(10, int(surface_width * 0.012))

    bottom_height = get_bottom_height(surface)

    bottom = pygame.Rect(0, surface_height - bottom_height, surface_width, bottom_height)
    pygame.draw.rect(surface, (255, 255, 255), bottom)
    pygame.draw.line(surface, (0, 0, 0), (bottom.x, bottom.y), (bottom.right, bottom.y), width=2)

    try:
        label = player.name
    except AttributeError:
        label = "Player"
    surface.blit(font.render(f"{label} hand:", True, (0, 0, 0)), (18, bottom.y + 10))

    x = 18
    y = bottom.y + 10 + font.get_height() + 10

    for resource_key, sprite_key in cards:
        cache_key = (sprite_key, card_width, card_height)
        img = card_cache.get(cache_key)
        if img is None:
            base = get_card_image(sprite_key)
            img = pygame.transform.scale(base, (card_width, card_height))
            card_cache[cache_key] = img

        surface.blit(img, (x, y))
        count = 0
        try:
            count = int(player.resources.get(resource_key, 0))
        except Exception:
            count = 0

        surface.blit(
            font.render(f"x{count}", True, (0, 0, 0)),
            (x + int(card_width * 0.30), y + card_height + 6),
        )
        x += card_width + gap
    
    
def draw_background(surface):
    # create a blue gradient background for the game
    width, height = surface.get_size()
    bg = pygame.Surface((width, height))
    for i in range(height):
        t = i / height
        red = int(30 + 10 * t)
        green = int(140 + 40 * t)
        blue = int(200 + 40 * t)
        pygame.draw.line(bg, (red, green, blue), (0, i), (width, i))
    surface.blit(bg, (0, 0))


def draw_action_bar(surface, current_player, phase="GAME", last_roll=None, message=""):
    surface_width, surface_height = surface.get_size()
    height = get_top_height(surface)
    bar = pygame.Rect(0, 0, surface_width, height)

    pygame.draw.rect(surface, (255, 255, 255), bar)
    pygame.draw.line(surface, (0, 0, 0), (bar.x, bar.bottom - 1), (bar.right, bar.bottom - 1), width=2)

    font = pygame.font.SysFont("trebuchet ms", max(16, int(height * 0.45)), bold=True)

    try:
        name = current_player.name
    except AttributeError:
        name = "Player"

    left_text = f"{name}'s turn"

    surface.blit(font.render(left_text, True, (0, 0, 0)), (18, (height - font.get_height()) // 2))

    if message:
        msg_font = pygame.font.SysFont("trebuchet ms", max(16, int(height * 0.55)), bold=True)
        msg_txt = msg_font.render(str(message), True, (0, 0, 0))
        surface.blit(msg_txt, msg_txt.get_rect(center=(surface_width // 2, height // 2)))
        return height

    # Rolled text centered in the action bar.
    if last_roll is not None:
        roll_font = pygame.font.SysFont("trebuchet ms", max(16, int(height * 0.50)), bold=True)
        roll_txt = roll_font.render(f"{name} rolled {last_roll}", True, (0, 0, 0))
        surface.blit(roll_txt, roll_txt.get_rect(center=(surface_width // 2, height // 2)))

    return height


def draw_player_list(surface, players, top=0):
    surface_width, surface_height = surface.get_size()
    pad = 14
    top = int(top)

    font = pygame.font.SysFont("trebuchet ms", max(14, int(surface_width * 0.015)))
    title_font = pygame.font.SysFont("trebuchet ms", max(15, int(surface_width * 0.016)), bold=True)

    panel_w = min(int(surface_width * 0.34), 420)
    title_h = title_font.get_height()
    line_h = font.get_height() + 2
    panel_h = pad + title_h + 8 + max(1, len(players)) * line_h + pad

    rect = pygame.Rect(18, top + 12, panel_w, panel_h)

    pygame.draw.rect(surface, (255, 255, 255), rect, border_radius=10)
    pygame.draw.rect(surface, (0, 0, 0), rect, width=2, border_radius=10)

    x = rect.x + pad
    y = rect.y + pad
    surface.blit(title_font.render("Game Stats", True, (0, 0, 0)), (x, y))
    y += title_h + 8

    swatch = max(10, int(line_h * 0.75))
    color_rect = pygame.Rect(0, 0, swatch, swatch)

    for player in players:
        try:
            name = player.name
        except AttributeError:
            name = "Player"

        try:
            pid = int(player.player_id or 0)
        except Exception:
            pid = 0

        color = consts.PlayerColors.get(pid, (0, 0, 0))

        try:
            vp = int(player.points)
        except Exception:
            vp = 0

        try:
            cards = int(player.get_card_count())
        except Exception:
            cards = 0

        color_rect.topleft = (x, y + (line_h - swatch) // 2)
        pygame.draw.rect(surface, color, color_rect)
        pygame.draw.rect(surface, (0, 0, 0), color_rect, width=2)

        line = f"{name}:  VP {vp}  |  Cards {cards}"
        surface.blit(font.render(line, True, (0, 0, 0)), (x + swatch + 10, y))
        y += line_h

    return rect


# PLAYER UI

def draw_button_rects(surface, bottom=0):
    """Compute button rectangles for the left-side action column."""
    buttons = [
        ("dice_roll", "Dice Roll"),
        ("trade", "Trade"),
        ("dev_card", "Dev Card"),
        ("use_knight", "Use Knight"),
        ("road", "Road"),
        ("settlement", "Settlement"),
        ("city", "City"),
        ("end_turn", "End Turn"),
    ]

    screen_width = surface.get_width()
    screen_height = surface.get_height()

    button_height = int(screen_height * 0.05)
    button_width = int(screen_width * 0.12)
    button_spacing = int(screen_height * 0.015)

    x = 18

    total_height = len(buttons) * (button_height + button_spacing)

    bottom_margin = int(bottom) - 70

    y = screen_height - int(bottom) - total_height


    rects = {}
    for key, label in buttons:
        rects[key] = pygame.Rect(x, y, button_width, button_height)
        y += button_height + button_spacing

    return rects


def draw_player_buttons(surface, bottom=0, last_roll=None, active_mode=None, current_player=None):
    rects = draw_button_rects(surface, bottom=bottom)

    labels = {
        "dice_roll": "Dice Roll",
        "trade": "Trade",
        "dev_card": "Dev Card",
        "use_knight": "Use Knight",
        "road": "Road",
        "settlement": "Settlement",
        "city": "City",
        "end_turn": "End Turn",
    }

    # Button enablement rules.
    player = current_player

    for key, rect in rects.items():
        is_active = (active_mode is not None and key == active_mode)
        enabled = True

        if player is not None:
            try:
                has_rolled = bool(player.has_rolled)
            except Exception:
                has_rolled = False

            if key == "dice_roll":
                enabled = (not has_rolled)
            elif key == "use_knight":
                try:
                    enabled = int(player.resources.get("dev", 0)) > 0
                except Exception:
                    enabled = False
            elif key in ("road", "settlement", "city", "dev_card"):
                enabled = has_rolled
            elif key == "end_turn":
                enabled = has_rolled

            # Also require affordability + piece limits for build actions.
            if enabled and key == "road":
                try:
                    enabled = player.buy_item("road", spend=False) and int(player.structures.get("roads", 0)) < 15
                except Exception:
                    enabled = False
            if enabled and key == "settlement":
                try:
                    enabled = player.buy_item("settlement", spend=False) and int(player.structures.get("settlements", 0)) < 5
                except Exception:
                    enabled = False
            if enabled and key == "city":
                try:
                    enabled = player.buy_item("city", spend=False) and int(player.structures.get("cities", 0)) < 4
                except Exception:
                    enabled = False
            if enabled and key == "dev_card":
                try:
                    enabled = player.buy_item("dev_card", spend=False)
                except Exception:
                    enabled = False

        draw_button(
            surface,
            rect.x,
            rect.y,
            rect.width,
            rect.height,
            labels.get(key, key),
            active=is_active,
            enabled=enabled,
        )

    return rects


def draw_local_player(surface, local_player):
    x = surface.get_width() * 0.03
    y = surface.get_height() - 100

    pygame.draw.rect(surface, (0, 200, 0), (x, y, 520, 60), border_radius=8)

    text = font.render(
        f"{local_player.name}: "
        f"{local_player.get_card_count()} cards, "
        f"{local_player.points} victory points",
        True,
        BLACK
    )
    surface.blit(text, (x + 10, y + 20))


# HELPER UI FUNCTIONS

def draw_button(surface, x, y, width, height, text, active=False, enabled=True):
    rect = pygame.Rect(x, y, width, height)
    fill = WHITE
    if active:
        fill = (225, 225, 225)
    if not enabled:
        fill = (200, 200, 200)
    pygame.draw.rect(surface, fill, rect, border_radius=10)
    pygame.draw.rect(surface, (0, 0, 0), rect, width=2, border_radius=10)
    text_color = BLACK
    if not enabled:
        text_color = (120, 120, 120)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(label, label_rect)


def draw_exit_button(surface):
    exit_button = pygame.image.load("sprites/exit_button.png").convert_alpha()
    exit_button = pygame.transform.scale(exit_button, (40, 40))

    x = surface.get_width() - 60
    # Center the exit button inside the action bar.
    y = (get_top_height(surface) - 40) // 2
    surface.blit(exit_button, (x, y))

    exit_rect = pygame.Rect(x, y, 40, 40)
    if pygame.mouse.get_pressed()[0] and exit_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.quit()
        raise SystemExit


def draw_end_screen(surface, winner_name):
    surface_width, surface_height = surface.get_size()

    bg = get_menu_background(surface)
    if bg is not None:
        surface.blit(bg, (0, 0))
    else:
        surface.fill(BLUE)

    title_font = pygame.font.SysFont("trebuchet ms", max(48, int(surface_height * 0.10)), bold=True)
    sub_font = pygame.font.Font(None, max(28, int(surface_height * 0.05)))
    btn_font = pygame.font.Font(None, max(36, int(surface_height * 0.05)))

    title = title_font.render("Conquistador", True, WHITE)
    surface.blit(title, title.get_rect(center=(surface_width // 2, surface_height // 4)))

    win_text = sub_font.render(f"{winner_name} wins!", True, WHITE)
    surface.blit(win_text, win_text.get_rect(center=(surface_width // 2, int(surface_height * 0.40))))

    hint_text = sub_font.render("First to 10 victory points", True, WHITE)
    surface.blit(hint_text, hint_text.get_rect(center=(surface_width // 2, int(surface_height * 0.47))))

    button_w = 240
    button_h = 56
    gap = 18

    menu_button = pygame.Rect(0, 0, button_w, button_h)
    quit_button = pygame.Rect(0, 0, button_w, button_h)

    menu_button.center = (surface_width // 2, int(surface_height * 0.58))
    quit_button.center = (surface_width // 2, int(surface_height * 0.58) + button_h + gap)

    mouse_pos = pygame.mouse.get_pos()

    menu_color = GREEN
    if menu_button.collidepoint(mouse_pos):
        menu_color = GRAY
    quit_color = GREEN
    if quit_button.collidepoint(mouse_pos):
        quit_color = GRAY

    pygame.draw.rect(surface, menu_color, menu_button)
    pygame.draw.rect(surface, quit_color, quit_button)

    pygame.draw.rect(surface, BLACK, menu_button, width=2)
    pygame.draw.rect(surface, BLACK, quit_button, width=2)

 ##   menu_label = btn_font.render("Main Menu", True, BLACK)
    quit_label = btn_font.render("Quit", True, BLACK)
   ## surface.blit(menu_label, menu_label.get_rect(center=menu_button.center))
    surface.blit(quit_label, quit_label.get_rect(center=quit_button.center))

    return menu_button, quit_button
        
        
def get_bottom_height(surface):
    surface_width, surface_height = surface.get_size()
    font = pygame.font.SysFont("trebuchet ms", max(14, int(surface_width * 0.015)))

    card_width = max(50, int(surface_width * 0.045))
    card_height = int(card_width * 1.35)

    required_height = 10 + font.get_height() + 12 + card_height + font.get_height() + 18
    return max(required_height, int(surface_height * 0.18))