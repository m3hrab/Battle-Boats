import pygame 

class Button():

    def __init__(self, position, size):
        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)