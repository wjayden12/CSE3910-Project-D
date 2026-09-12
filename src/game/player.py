import random


class Player:
    def __init__(self, name, points=0, road_length=0, player_id=None, color=(0, 0, 0)):
        self.name = name
        self.points = points
        self.road_length = road_length
        self.player_id = player_id
        self.color = color

        self.has_rolled = False
        self.rolled_value = None
        self.has_longest_road = False
        self.knights_used = 0

        # Player resources
        self.resources = {
            "wood": 0,
            "brick": 0,
            "sheep": 0,
            "wheat": 0,
            "ore": 0,
            "dev": 0,
        }

        # Player structures
        self.structures = {
            "roads": 0,
            "settlements": 0,
            "cities": 0
        }

        # Costs for building
        self.costs = {
            "road": {"wood": 1, "brick": 1},
            "settlement": {"wood": 1, "brick": 1, "sheep": 1, "wheat": 1},
            "city": {"ore": 3, "wheat": 2},
            "dev_card": {"sheep": 1, "wheat": 1, "ore": 1},
        }

    # Buying logic
    def can_afford(self, cost):
        for r, c in cost.items():
            if self.resources.get(r, 0) < c:
                return False
        return True

    def spend(self, cost):
        for r, c in cost.items():
            self.resources[r] -= c

    def buy_item(self, item, spend=True):
        cost = self.costs.get(item)
        if cost is None:
            return False

        if not self.can_afford(cost):
            return False

        if spend:
            self.spend(cost)

            # ----- structure accounting -----
            if item == "road":
                self.structures["roads"] += 1

            elif item == "settlement":
                self.structures["settlements"] += 1

            elif item == "city":
                # city must upgrade an existing settlement
                if self.structures["settlements"] <= 0:
                    # rollback spend if you want stricter safety:
                    # for r, c in cost.items():
                    #     self.resources[r] += c
                    return False
                self.structures["settlements"] -= 1
                self.structures["cities"] += 1

        return True

    # Dice rolling
    def roll_dice(self):
        if self.has_rolled:
            return None
        self.rolled_value = random.randint(1, 6) + random.randint(1, 6)
        self.has_rolled = True
        return self.rolled_value

    # Turn management
    def start_turn(self):
        self.has_rolled = False
        self.rolled_value = None

    # UI interaction
    def handle_click(self, button_rects, mouse_pos):
        # Roll dice
        dice_rect = button_rects.get("dice_roll")
        if dice_rect and dice_rect.collidepoint(mouse_pos):
            if not self.has_rolled:
                roll = self.roll_dice()
                return "dice_roll", roll
            return None, None

        # Build road
        road_rect = button_rects.get("road")
        if road_rect and road_rect.collidepoint(mouse_pos):
            return "select_build", "road"

        # Build settlement
        settlement_rect = button_rects.get("settlement")
        if settlement_rect and settlement_rect.collidepoint(mouse_pos):
            return "select_build", "settlement"

        # Build city
        city_rect = button_rects.get("city")
        if city_rect and city_rect.collidepoint(mouse_pos):
            return "select_build", "city"

        # Buy development card
        dev_rect = button_rects.get("dev_card")
        if dev_rect and dev_rect.collidepoint(mouse_pos):
            return "buy_dev", None

        # Use knight card
        knight_rect = button_rects.get("use_knight")
        if knight_rect and knight_rect.collidepoint(mouse_pos):
            if self.resources.get("dev", 0) > 0:
                return "use_knight", None
            return None, None

        # End turn
        end_rect = button_rects.get("end_turn")
        if end_rect and end_rect.collidepoint(mouse_pos):
            if self.has_rolled:
                return "end_turn", None
            return None, None

        return None, None

    # Utilities
    def get_card_count(self):
        return sum(self.resources.values())

    def __repr__(self):
        return f"{self.name}: {self.get_card_count()} cards, {self.points} victory points"

# Bank for trading
class Bank:
    def __init__(self):
        self.items = {
            "brick": 19,
            "wood": 19,
            "wheat": 19,
            "sheep": 19,
            "ore": 19,
            "dev": 25,
        }

    def trade_4_to_1(self, player, give, receive):
        if player.resources.get(give, 0) < 4:
            return False
        if self.items.get(receive, 0) <= 0:
            return False

        player.resources[give] -= 4
        player.resources[receive] += 1

        self.items[give] += 4
        self.items[receive] -= 1
        return True
