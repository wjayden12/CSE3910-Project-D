import pygame

from src.game.constants import BLUE, WHITE, GRAY, GREEN, BLACK

pygame.font.init()
menu_font = pygame.font.SysFont("trebuchet ms", 150)
small_font = pygame.font.Font(None, 50)

game_state = "MENU"

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def get_button_collision(rect, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rect.collidepoint(event.pos):
            return True
    return False

def draw_menu(screen, screen_width, screen_height):
    global game_state

    try:
        bg_image = pygame.image.load("sprites/catan_bg.png").convert()
        bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    except pygame.error:
        bg_image = None

    # try loading conquistador title image, if it doesn't work then load it normally
    try:
        title_image = pygame.image.load("sprites/conquistador.png").convert_alpha()

        max_width = int(screen_width * 0.8)
        max_height = int(screen_height * 0.4)
        origin_width, origin_height = title_image.get_size()

        if origin_width > 0 and origin_height > 0:
            scale = min(max_width / origin_width, max_height / origin_height, 1.0)
            if scale != 1.0:
                new_size = (max(1, int(origin_width * scale)), max(1, int(origin_height * scale)))
                title_image = pygame.transform.smoothscale(title_image, new_size)
    except FileNotFoundError:
        title_image = None

    while game_state == "MENU":
        # load background image
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(BLUE)

        # load title image
        if title_image:
            title_rect = title_image.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(title_image, title_rect)
        else:
            draw_text('Conquistador', menu_font, WHITE, screen, screen_width // 2, screen_height // 4)

        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        left_click = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True

        play_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 70, 200, 50)

        # change button colour on hover
        if play_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GRAY, play_button)
            if left_click:
                game_state = "GAME"
        else:
            pygame.draw.rect(screen, GREEN, play_button)

        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GRAY, exit_button)
            if left_click:
                pygame.quit()
                raise SystemExit
        else:
            pygame.draw.rect(screen, GREEN, exit_button)

        draw_text('Play', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 25)
        draw_text('Exit', small_font, BLACK, screen, screen_width // 2, screen_height // 2 + 95)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if get_button_collision(play_button, event):
                return "start"

            if get_button_collision(exit_button, event):
                exit()
    return None
