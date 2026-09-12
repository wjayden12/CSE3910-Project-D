import pygame

from src.ui.menu import draw_menu
from src.game.game import Game


def main():
    pygame.init()

    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Conquistador")

    pygame.font.init()

    pygame.mixer.music.load("src/audio/song.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    state = "MENU"

    while state != "EXIT":
        if state == "MENU":
            result = draw_menu(screen, screen_width, screen_height)

            if result == "start":
                state = "GAME"
            elif result == "quit":
                state = "EXIT"

        elif state == "GAME":
            game = Game()

            while game.running:
                for event in pygame.event.get():
                    game.handle_event(event, screen)

                game.draw(screen)

                pygame.display.update()
                clock.tick(60)
            
            # has the player exited to the menu or quit the game?
            exit_menu = False
            quit_game = False
            
            try:
                exit_menu = bool(game.exit_menu)
            except Exception:
                exit_menu = False
            try:
                quit_game = bool(game.quit_game)
            except Exception:
                quit_game = False

            if exit_menu:
                state = "MENU"
            elif quit_game:
                state = "EXIT"
            else:
                state = "EXIT"

    # if state is exit then stop music and quit game
    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
