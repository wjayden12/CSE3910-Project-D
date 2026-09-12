import random

counts = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]


def generate_counts(row_counts):
    max_cols = max(row_counts)
    x_positions = {}
    for row_index, cols in enumerate(row_counts):
        offset = (max_cols - cols) / 2.0
        for column_index in range(cols):
            x_positions[(row_index, column_index)] = offset + column_index

    neighbors = {}
    for cell in x_positions:
        neighbors[cell] = []

    for row_index, cols in enumerate(row_counts):
        for column_index in range(cols):
            if column_index - 1 >= 0:
                neighbors[(row_index, column_index)].append((row_index, column_index - 1))
            if column_index + 1 < cols:
                neighbors[(row_index, column_index)].append((row_index, column_index + 1))

    # cross-row adjacency
    for row_index in range(len(row_counts) - 1):
        cols_a = row_counts[row_index]
        cols_b = row_counts[row_index + 1]
        for column_index_a in range(cols_a):
            x_pos_a = x_positions[(row_index, column_index_a)]
            for column_index_b in range(cols_b):
                x_pos_b = x_positions[(row_index + 1, column_index_b)]
                if abs(abs(x_pos_a - x_pos_b) - 0.5) < 1e-9:
                    neighbors[(row_index, column_index_a)].append((row_index + 1, column_index_b))
                    neighbors[(row_index + 1, column_index_b)].append((row_index, column_index_a))

    return neighbors


def draw_counts(tiles, row_counts):
    neighbors = generate_counts(row_counts)

    non_desert_cells = []
    for row_index, row in enumerate(tiles):
        for column_index, tile in enumerate(row):
            if tile.resource_type != "desert":
                non_desert_cells.append((row_index, column_index))
            else:
                tile.count = None

    if len(non_desert_cells) != len(counts):
        return

    shuffled_counts = list(counts)

    def check_counts():
        for (row_index, column_index) in non_desert_cells:
            tile_count = tiles[row_index][column_index].count
            if tile_count not in (6, 8):
                continue
            for (neighbor_row, neighbor_column) in neighbors[(row_index, column_index)]:
                neighbor_tile_count = tiles[neighbor_row][neighbor_column].count
                if neighbor_tile_count in (6, 8):
                    return False
        return True

    for _ in range(2000):
        random.shuffle(shuffled_counts)
        for idx, (row_index, column_index) in enumerate(non_desert_cells):
            tiles[row_index][column_index].count = shuffled_counts[idx]
        if check_counts():
            return
    return


class Tile:
    def __init__(self, capacity, resource_type="desert", count=None):
        self.capacity = capacity
        self.resource_type = resource_type
        self.count = count

    def get_resource_type(self):
        return self.resource_type

    def get_capacity(self):
        return self.capacity

def build_tiles(row_counts=None):
    # top and bottom row = 3 tiles, converging to 5 tiles in the middle
    if row_counts is None:
        row_counts = [3, 4, 5, 4, 3]

    # average distribution of each tile
    tile_counts = {
        "lumber": 4,
        "brick": 3,
        "wool": 4,
        "grain": 4,
        "ore": 3,
        "desert": 1,
    }

    resources = []
    for resource_type, count in tile_counts.items():
        resources.extend([resource_type] * count)

    # shuffle tiles
    random.shuffle(resources)

    # build tiles
    tiles = []
    index = 0
    for count in row_counts:
        row = []
        for _ in range(count):
            resource_type = resources[index]
            index += 1
            row.append(Tile(capacity=0, resource_type=resource_type))
        tiles.append(row)

    draw_counts(tiles, row_counts)

    return tiles

        