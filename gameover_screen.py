import pygame 
from button import Button

class GameOverScreen():

    def __init__(self, screen, settings) -> None:
        self.screen = screen
        self.settings = settings
        self.winner = None
        self.bg = pygame.image.load("assets/images/game_over.png")
        # Play again button at center of screen
        self.play_again_button = Button((self.settings.screen_width/2 - 50, self.settings.screen_height/2), (100, 50))
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_button.rect.collidepoint(event.pos):
                    return "game"
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "game"
                
    def draw_winner(self):
        if self.winner == "player":
            text = self.settings.text_font.render("Congratulations! You won!", True, (255, 255, 255))
        else:
            text = self.settings.text_font.render("Opps! You lose!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.settings.screen_width/2, self.settings.screen_height/2))
        self.screen.blit(text, text_rect)
        
    def draw(self):
        # light blue background
        self.screen.blit(self.bg, (0, 0))
        self.draw_winner()
        self.play_again_button.draw(self.screen)