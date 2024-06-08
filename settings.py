import pygame 

class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 960
        self.screen_height = 540
        self.caption = "Battle Boats"

        # Fonts 
        self.text_font = pygame.font.Font("assets/fonts/Anton-Regular.ttf", 36)
        self.button_font = pygame.font.Font("assets/fonts/Anton-Regular.ttf", 16)

        # Game settings
        self.grid_size = 10
        self.cell_size = 35
        self.margin = 70
        self.player_grid_start_x = self.margin
        self.player_grid_start_y = self.margin + 20

        self.ai_grid_start_x = self.screen_width - self.margin - self.grid_size * self.cell_size
        self.ai_grid_start_y = self.margin + 20        

