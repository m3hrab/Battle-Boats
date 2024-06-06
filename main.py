import pygame
import sys
from settings import Settings
from start_screen import StartScreen
from game_screen import GameScreen

def run():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)

    start_screen = StartScreen(screen)
    game_screen = GameScreen(screen, settings)
    
    current_screen = game_screen
    while True:
        
        events = pygame.event.get()
        flag = current_screen.handle_events(events)
        if flag == "quit":
            sys.exit()

        current_screen.draw()

        pygame.display.flip()


if __name__ == '__main__':
    run()