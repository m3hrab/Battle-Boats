class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 960
        self.screen_height = 540
        self.caption = "Battle Boats"

        # Game settings
        self.grid_size = 10
        self.cell_size = 38
        self.margin = 60
        self.player_grid_start_x = self.margin
        self.player_grid_start_y = self.margin + 20

        self.ai_grid_start_x = self.screen_width - self.margin - self.grid_size * self.cell_size
        self.ai_grid_start_y = self.margin + 20        

