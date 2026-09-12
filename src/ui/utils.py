import pygame

tile_files = {
    "brick": "brick_tile.png",
    "grain": "grain_tile.png",
    "wool": "wool_tile.png",
    "lumber": "lumber_tile.png",
    "ore": "ore_tile.png",
    "desert": "desert_tile.png",
}

card_files = {
    "brick": "brick_card.png",
    "grain": "grain_card.png",
    "lumber": "lumber_card.png",
    "ore": "ore_card.png",
    "wool": "wool_card.png",
    "dev": "dev_card.png",
}

tile_cache = {}
card_cache = {}


# function to fetch each tile .png file and format it
def get_tile_image(resource_type):
    if resource_type not in tile_files:
        resource_type = "desert"

    cached = tile_cache.get(resource_type)
    if cached is not None:
        return cached

    file_name = tile_files[resource_type]
    path = "sprites/tiles/" + file_name
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (200, 200))
    tile_cache[resource_type] = image
    return image


def get_card_image(card_type):
    if card_type not in card_files:
        card_type = "dev"

    cached = card_cache.get(card_type)
    if cached is not None:
        return cached

    file_name = card_files[card_type]
    path = "sprites/cards/" + file_name
    image = pygame.image.load(path).convert_alpha()
    card_cache[card_type] = image
    return image
