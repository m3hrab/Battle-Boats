import pygame

class StartScreen():

    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.image.load('assets/images/start_window.png')

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()