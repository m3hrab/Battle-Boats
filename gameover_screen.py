import pygame 
from button import Button

class GameOverScreen():

    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.winner = None

        # Play again button at center of screen
        self.play_again_button = Button((self.settings.screen_width/2 - 50, self.settings.screen_height/2), (100, 50))
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_button.rect.collidepoint(event.pos):
                    return "game"
                
    def draw_winner(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"{self.winner} wins!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
        self.screen.blit(text, text_rect)
        
    def draw(self):
        # light blue background
        self.screen.fill((135, 206, 250))
        self.draw_winner()
        self.play_again_button.draw(self.screen)