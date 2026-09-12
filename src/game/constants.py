# colour constants

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (45, 185, 250)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

CENTER = (420, 295)
RESOURCE_RADIUS = 50

# tile positions
"""
TilePositions is a dictionary containing the (x, y) coordinates for each of the tiles on the game board
To create this dictionary I calculated the center point of the board and then used AI to help me figure out the relative positions of each tile based on the resource radius
"""
TilePositions = {
    0: (CENTER[0] - 2 * RESOURCE_RADIUS, CENTER[1] - 4 * RESOURCE_RADIUS),
    1: (CENTER[0], CENTER[1] - 4 * RESOURCE_RADIUS),
    2: (CENTER[0] + 2 * RESOURCE_RADIUS, CENTER[1] - 4 * RESOURCE_RADIUS),
    11: (CENTER[0] - 3 * RESOURCE_RADIUS, CENTER[1] - 2 * RESOURCE_RADIUS),
    12: (CENTER[0] - RESOURCE_RADIUS, CENTER[1] - 2 * RESOURCE_RADIUS),
    13: (CENTER[0] + RESOURCE_RADIUS, CENTER[1] - 2 * RESOURCE_RADIUS),
    3: (CENTER[0] + 3 * RESOURCE_RADIUS, CENTER[1] - 2 * RESOURCE_RADIUS),
    10: (CENTER[0] - 4 * RESOURCE_RADIUS, CENTER[1]),
    17: (CENTER[0] - 2 * RESOURCE_RADIUS, CENTER[1]),
    18: (CENTER[0], CENTER[1]),
    14: (CENTER[0] + 2 * RESOURCE_RADIUS, CENTER[1]),
    4: (CENTER[0] + 4 * RESOURCE_RADIUS, CENTER[1]),
    9: (CENTER[0] - 3 * RESOURCE_RADIUS, CENTER[1] + 2 * RESOURCE_RADIUS),
    16: (CENTER[0] - RESOURCE_RADIUS, CENTER[1] + 2 * RESOURCE_RADIUS),
    15: (CENTER[0] + RESOURCE_RADIUS, CENTER[1] + 2 * RESOURCE_RADIUS),
    5: (CENTER[0] + 3 * RESOURCE_RADIUS, CENTER[1] + 2 * RESOURCE_RADIUS),
    8: (CENTER[0] - 2 * RESOURCE_RADIUS, CENTER[1] + 4 * RESOURCE_RADIUS),
    7: (CENTER[0], CENTER[1] + 4 * RESOURCE_RADIUS),
    6: (CENTER[0] + 2 * RESOURCE_RADIUS, CENTER[1] + 4 * RESOURCE_RADIUS),
}

# settlement placement positions
"""
SettlementPositions is a dictionary containing the (x, y) coordinates for each of the settlement positions on the game board, created in the same manner as TilePositions
"""
SettlementPositions = {
    0: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] - 4.75 * RESOURCE_RADIUS)),
    1: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] - 5.25 * RESOURCE_RADIUS)),
    2: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] - 4.75 * RESOURCE_RADIUS)),
    3: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] - 5.25 * RESOURCE_RADIUS)),
    4: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] - 4.75 * RESOURCE_RADIUS)),
    5: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] - 5.25 * RESOURCE_RADIUS)),
    6: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] - 4.75 * RESOURCE_RADIUS)),
    7: (CENTER[0] - 4 * RESOURCE_RADIUS, int(CENTER[1] - 2.75 * RESOURCE_RADIUS)),
    8: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] - 3.25 * RESOURCE_RADIUS)),
    9: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] - 2.75 * RESOURCE_RADIUS)),
    10: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] - 3.25 * RESOURCE_RADIUS)),
    11: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] - 2.75 * RESOURCE_RADIUS)),
    12: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] - 3.25 * RESOURCE_RADIUS)),
    13: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] - 2.75 * RESOURCE_RADIUS)),
    14: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] - 3.25 * RESOURCE_RADIUS)),
    15: (CENTER[0] + 4 * RESOURCE_RADIUS, int(CENTER[1] - 2.75 * RESOURCE_RADIUS)),
    16: (CENTER[0] - 5 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    17: (CENTER[0] - 4 * RESOURCE_RADIUS, int(CENTER[1] - 1.25 * RESOURCE_RADIUS)),
    18: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    19: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] - 1.25 * RESOURCE_RADIUS)),
    20: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    21: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] - 1.25 * RESOURCE_RADIUS)),
    22: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    23: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] - 1.25 * RESOURCE_RADIUS)),
    24: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    25: (CENTER[0] + 4 * RESOURCE_RADIUS, int(CENTER[1] - 1.25 * RESOURCE_RADIUS)),
    26: (CENTER[0] + 5 * RESOURCE_RADIUS, int(CENTER[1] - 0.75 * RESOURCE_RADIUS)),
    27: (CENTER[0] - 5 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    28: (CENTER[0] - 4 * RESOURCE_RADIUS, int(CENTER[1] + 1.25 * RESOURCE_RADIUS)),
    29: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    30: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] + 1.25 * RESOURCE_RADIUS)),
    31: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    32: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] + 1.25 * RESOURCE_RADIUS)),
    33: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    34: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] + 1.25 * RESOURCE_RADIUS)),
    35: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    36: (CENTER[0] + 4 * RESOURCE_RADIUS, int(CENTER[1] + 1.25 * RESOURCE_RADIUS)),
    37: (CENTER[0] + 5 * RESOURCE_RADIUS, int(CENTER[1] + 0.75 * RESOURCE_RADIUS)),
    38: (CENTER[0] - 4 * RESOURCE_RADIUS, int(CENTER[1] + 2.75 * RESOURCE_RADIUS)),
    39: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] + 3.25 * RESOURCE_RADIUS)),
    40: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] + 2.75 * RESOURCE_RADIUS)),
    41: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] + 3.25 * RESOURCE_RADIUS)),
    42: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] + 2.75 * RESOURCE_RADIUS)),
    43: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] + 3.25 * RESOURCE_RADIUS)),
    44: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] + 2.75 * RESOURCE_RADIUS)),
    45: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] + 3.25 * RESOURCE_RADIUS)),
    46: (CENTER[0] + 4 * RESOURCE_RADIUS, int(CENTER[1] + 2.75 * RESOURCE_RADIUS)),
    47: (CENTER[0] - 3 * RESOURCE_RADIUS, int(CENTER[1] + 4.75 * RESOURCE_RADIUS)),
    48: (CENTER[0] - 2 * RESOURCE_RADIUS, int(CENTER[1] + 5.25 * RESOURCE_RADIUS)),
    49: (CENTER[0] - 1 * RESOURCE_RADIUS, int(CENTER[1] + 4.75 * RESOURCE_RADIUS)),
    50: (CENTER[0] + 0 * RESOURCE_RADIUS, int(CENTER[1] + 5.25 * RESOURCE_RADIUS)),
    51: (CENTER[0] + 1 * RESOURCE_RADIUS, int(CENTER[1] + 4.75 * RESOURCE_RADIUS)),
    52: (CENTER[0] + 2 * RESOURCE_RADIUS, int(CENTER[1] + 5.25 * RESOURCE_RADIUS)),
    53: (CENTER[0] + 3 * RESOURCE_RADIUS, int(CENTER[1] + 4.75 * RESOURCE_RADIUS)),
}

# roads are defined by the two vertices (settlement positions) they connect
roads = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
    (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),
    (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26),
    (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 34), (34, 35), (35, 36), (36, 37),
    (38, 39), (39, 40), (40, 41), (41, 42), (42, 43), (43, 44), (44, 45), (45, 46),
    (47, 48), (48, 49), (49, 50), (50, 51), (51, 52), (52, 53),

    # vertical / diagonals linking rows
    (0, 8), (2, 10), (4, 12), (6, 14),
    (7, 17), (9, 19), (11, 21), (13, 23), (15, 25),
    (16, 27), (18, 29), (20, 31), (22, 33), (24, 35), (26, 37),
    (28, 38), (30, 40), (32, 42), (34, 44), (36, 46),
    (39, 47), (41, 49), (43, 51), (45, 53),
]

# map each tile to their settlement positions
TileSettlementMap = {
    0: [0, 1, 2, 8, 9, 10],
    1: [2, 3, 4, 10, 11, 12],
    2: [4, 5, 6, 12, 13, 14],

    11: [7, 8, 9, 17, 18, 19],
    12: [9, 10, 11, 19, 20, 21],
    13: [11, 12, 13, 21, 22, 23],
    3: [13, 14, 15, 23, 24, 25],

    10: [16, 17, 18, 27, 28, 29],
    17: [18, 19, 20, 29, 30, 31],
    18: [20, 21, 22, 31, 32, 33],
    14: [22, 23, 24, 33, 34, 35],
    4: [24, 25, 26, 35, 36, 37],

    9: [28, 29, 30, 38, 39, 40],
    16: [30, 31, 32, 40, 41, 42],
    15: [32, 33, 34, 42, 43, 44],
    5: [34, 35, 36, 44, 45, 46],

    8: [39, 40, 41, 47, 48, 49],
    7: [41, 42, 43, 49, 50, 51],
    6: [43, 44, 45, 51, 52, 53],
}

# player colours
PlayerColors = {
    1: RED,     # red
    2: BLUE,    # blue
    3: GREEN,   # green
    4: YELLOW,  # yellow
}
