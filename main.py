import pygame
import sys
# game settings
from settings import Settings

# Game screens
from start_screen import StartScreen
from game_screen import GameScreen
from gameover_screen import GameOverScreen

def run():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)

    start_screen = StartScreen(screen)
    game_screen = GameScreen(screen, settings)
    gameover_screen = GameOverScreen(screen, settings)
    
    current_screen = game_screen

    while True:
        
        events = pygame.event.get()
        flag = current_screen.handle_events(events)
        if flag == "quit":
            sys.exit()
        elif flag == "game":
            current_screen = game_screen
        elif flag == "gameover":
            gameover_screen.winner = game_screen.winner
            current_screen = gameover_screen

        current_screen.draw()

        pygame.display.flip()


if __name__ == '__main__':
    run()