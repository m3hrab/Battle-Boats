import pygame
import random
import time

class GameScreen:

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.bg = pygame.image.load('assets/images/game_bg.png')
        
        # Load ship images and create rotated versions for horizontal placement
        self.ships = [
            ("Aircraft Carrier", 5, 'assets/images/aircraftcarrier.png'),
            ("Battleship", 4, 'assets/images/battleship.png'),
            ("Cruiser", 4, 'assets/images/cruiser.png'),
            ("Submarine", 3, 'assets/images/submarine.png'),
            ("Destroyer", 2, 'assets/images/destroyer.png')
        ]
        
        self.ship_images = {}
        for name, size, image_path in self.ships:
            image = pygame.image.load(image_path)
            horizontal_image = pygame.transform.scale(image, (size * self.settings.cell_size, self.settings.cell_size))
            vertical_image = pygame.transform.rotate(horizontal_image, 90)
            self.ship_images[name] = {'horizontal': horizontal_image, 'vertical': vertical_image}

        self.player_grid = [[0] * self.settings.grid_size for _ in range(self.settings.grid_size)]
        self.ai_grid = [[0] * self.settings.grid_size for _ in range(self.settings.grid_size)]
        self.player_ships = []
        self.ai_ships = []
        
        self.current_ship_index = 0
        self.placing_horizontal = True

        self.place_ai_ships()
        self.game_started = False
        self.player_turn = False

        self.start_button = pygame.Rect(self.settings.screen_width // 2 - 50, self.settings.screen_height - 50, 92, 34)

        self.is_gameover = False
        self.winner = None
        self.flag = False

        # Load fire and water drop sprites and transform them to the cell size
        self.fire_sprites = [pygame.transform.scale(pygame.image.load(f'assets/images/fire_sprites/{i}.png'), (self.settings.cell_size, self.settings.cell_size)) for i in range(1, 5)]
        self.water_sprites = [pygame.transform.scale(pygame.image.load(f'assets/images/water_sprites/{i}.png'), (self.settings.cell_size, self.settings.cell_size)) for i in range(1, 5)]
        

        # Texts 
        self.text1 = self.settings.button_font.render("Your Fleet", True, (255, 255, 255))
        self.text2 = self.settings.button_font.render("Enemy's Fleet", True, (255, 255, 255))
        self.button_text = self.settings.button_font.render("START GAME", True, (255, 255, 255))

    def reset(self):
        self.player_grid = [[0] * self.settings.grid_size for _ in range(self.settings.grid_size)]
        self.ai_grid = [[0] * self.settings.grid_size for _ in range(self.settings.grid_size)]
        self.player_ships = []
        self.ai_ships = []
        self.current_ship_index = 0
        self.placing_horizontal = True
        self.place_ai_ships()
        self.game_started = False
        self.player_turn = False
        self.is_gameover = False


        
    def handle_events(self, events):
        for event in events:
            if self.is_gameover:
                self.reset()
                return "gameover"

            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not self.game_started:
                    if self.start_button.collidepoint(mouse_pos) and self.current_ship_index >= len(self.ships):
                        self.game_started = True
                        self.player_turn = False
                        self.ai_attack()
                    else:
                        player_cell = self.get_cell(mouse_pos, self.settings.player_grid_start_x, self.settings.player_grid_start_y)
                        if player_cell and self.current_ship_index < len(self.ships):
                            row, col = player_cell
                            ship_name, ship_size, _ = self.ships[self.current_ship_index]
                            if self.can_place_ship(self.player_grid, row, col, ship_size, self.placing_horizontal):
                                self.place_ship(self.player_grid, row, col, ship_size, self.placing_horizontal, ship_name)
                                self.player_ships.append((ship_name, ship_size, (row, col), self.placing_horizontal))
                                self.current_ship_index += 1

                else:
                    if self.player_turn:
                        ai_cell = self.get_cell(mouse_pos, self.settings.ai_grid_start_x, self.settings.ai_grid_start_y)
                        if ai_cell:
                            self.player_attack(ai_cell)
                            self.player_turn = False
                            # wait for 1 second before AI attacks
                            self.draw()
                            pygame.display.flip()
                            time.sleep(.3)
                            self.ai_attack()
                        
                        # print("Player Grid")
                        # for row in self.player_grid:
                        #     print(row)

                        # print("AI Grid")
                        # for row in self.ai_grid:
                        #     print(row)

                        # print(".............\n")
                

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.game_started:
                    self.placing_horizontal = not self.placing_horizontal

    def get_cell(self, mouse_pos, start_x, start_y):
        x, y = mouse_pos
        if start_x <= x < start_x + self.settings.grid_size * self.settings.cell_size and start_y <= y < start_y + self.settings.grid_size * self.settings.cell_size:
            col = (x - start_x) // self.settings.cell_size
            row = (y - start_y) // self.settings.cell_size
            return row, col
        return None

    def can_place_ship(self, grid, row, col, size, horizontal):
        if horizontal:
            if col + size > self.settings.grid_size:
                return False
            for i in range(size):
                if grid[row][col + i] != 0:
                    return False
        else:
            if row + size > self.settings.grid_size:
                return False
            for i in range(size):
                if grid[row + i][col] != 0:
                    return False
        return True

    def place_ship(self, grid, row, col, size, horizontal, ship_name):
        if ship_name == 'Aircraft Carrier':
            place = 5
        elif ship_name == 'Battleship':
            place = 4
        elif ship_name == 'Cruiser':
            place = 3
        elif ship_name == 'Submarine':
            place = 2
        elif ship_name == 'Destroyer':
            place = 1

        if horizontal:
            for i in range(size):
                grid[row][col + i] = place
        else:
            for i in range(size):
                grid[row + i][col] = place

    def place_ai_ships(self):
        for ship_name, ship_size, _ in self.ships:
            placed = False
            while not placed:
                row = random.randint(0, self.settings.grid_size - 1)
                col = random.randint(0, self.settings.grid_size - 1)
                horizontal = random.choice([True, False])
                if self.can_place_ship(self.ai_grid, row, col, ship_size, horizontal):
                    self.place_ship(self.ai_grid, row, col, ship_size, horizontal, ship_name)
                    self.ai_ships.append((ship_name, ship_size, (row, col), horizontal))
                    placed = True

    def ai_attack(self):
        while True:
            # choose from only those cell whose value is 0
            valid_cells = []
            for row in range(self.settings.grid_size):
                for col in range(self.settings.grid_size):
                    if self.player_grid[row][col] >= 0:
                        valid_cells.append((row, col))
            
            row, col = random.choice(valid_cells)

            if self.player_grid[row][col] == 0 or self.player_grid[row][col] == -6:
                self.player_grid[row][col] = -6
                print("AI missed")
                flag = False
                break
            elif self.player_grid[row][col] != 0 and self.player_grid[row][col] != -6:
                self.player_grid[row][col] = -self.player_grid[row][col]
                print("AI hit")
                # self.player_ships.remove((self.player_grid[row][col], 0, (row, col), True))
                flag = True
                break
        
        if flag:
            self.draw_animation((row, col), self.fire_sprites, True)
        else:
            self.draw_animation((row, col), self.water_sprites, True)


                
        self.check_winner()
        self.player_turn = True

    def player_attack(self, cell):
        # check if the cell is already attacked
        if self.ai_grid[cell[0]][cell[1]] < 0:
            print("Already attacked")
            return
        
        row, col = cell
        if self.ai_grid[row][col] == 0 or self.ai_grid[row][col] == -6:
            self.ai_grid[row][col] = -6
            print("Player missed")
            self.draw_animation(cell, self.water_sprites, False)
            
        elif self.ai_grid[row][col] > 0 and self.ai_grid[row][col] != -6:
            self.ai_grid[row][col] = - self.ai_grid[row][col]
            print("Player hit")
            self.draw_animation(cell, self.fire_sprites, False)

        self.check_winner()

    

    def check_winner(self):
        player_ships_left = any(cell > 0 for row in self.player_grid for cell in row)
        ai_ships_left = any(cell > 0 for row in self.ai_grid for cell in row)
        if not player_ships_left:
            print("AI wins")
            self.winner = "AI"
            self.is_gameover = True
        elif not ai_ships_left:
            print("Player wins")
            self.winner = "Player"
            self.is_gameover = True

    def draw_animation(self, cell, sprites, ai_attack=False):
        
        row, col = cell
        if ai_attack:
            x = self.settings.player_grid_start_x + col * self.settings.cell_size
            y = self.settings.player_grid_start_y + row * self.settings.cell_size
        else:
            x = self.settings.ai_grid_start_x + col * self.settings.cell_size
            y = self.settings.ai_grid_start_y + row * self.settings.cell_size

        for sprite in sprites:
            self.draw()
            self.screen.blit(sprite, (x, y))
            time.sleep(.1)
            pygame.display.flip()

    def draw_grid(self, start_x, start_y, grid, player_ships, flag, current_ship_info=None, ship_pos=None, horizontal=True):
        for row in range(self.settings.grid_size):
            for col in range(self.settings.grid_size):
                rect = pygame.Rect(start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)

                if grid[row][col] != -6 and grid[row][col] < 0:
                    # draw the transparent red overlay
                    overlay = pygame.Surface((self.settings.cell_size, self.settings.cell_size), pygame.SRCALPHA)
                    overlay.fill((255, 0, 0, 200))  # Add some transparency
                    self.screen.blit(overlay, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

                elif grid[row][col] == -6:
                    # draw the transparent blue overlay
                    overlay = pygame.Surface((self.settings.cell_size, self.settings.cell_size), pygame.SRCALPHA)
                    # overlay.fill((0, 0, 150, 128))  # Add some transparency low    
                    # light blue
                    overlay.fill((135, 206, 250, 128))
                    self.screen.blit(overlay, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))    
        if flag:
            for ship_name, ship_size, (row, col), ship_horizontal in player_ships:
                ship_image = self.ship_images[ship_name]['horizontal' if ship_horizontal else 'vertical']
                self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

        # Draw the particular ai ships whose all cells are negatives
        # aircraft carrier(check if five -5 in the AI Grid is in the grid then draw the aircraft carrier)
        else:
            for ship_name, ship_size, (row, col), ship_horizontal in self.ai_ships:
                count_5 = 0
                count_4 = 0
                count_3 = 0
                count_2 = 0
                count_1 = 0
                
                for i in self.ai_grid:
                    for j in i:
                        if j == -5:
                            count_5 += 1
                        elif j == -4:
                            count_4 += 1
                        elif j == -3:
                            count_3 += 1
                        elif j == -2:
                            count_2 += 1
                        elif j == -1:
                            count_1 += 1

                if count_1 == 2 and ship_name == 'Destroyer':
                    # print(self.ai_ships)
                    # print(self.ship_images)
                    if self.ai_ships[4][3]:
                        ship_image = self.ship_images['Destroyer']['horizontal']
                    else:
                        ship_image = self.ship_images['Destroyer']['vertical']
                    self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

                elif count_2 == 3 and ship_name == 'Submarine':
                    if self.ai_ships[3][3]:
                        ship_image = self.ship_images['Submarine']['horizontal']
                    else:
                        ship_image = self.ship_images['Submarine']['vertical']
                    self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

                elif count_3 == 4 and ship_name == 'Cruiser':
                    if self.ai_ships[2][3]:
                        ship_image = self.ship_images['Cruiser']['horizontal']
                    else:
                        ship_image = self.ship_images['Cruiser']['vertical']
                    self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))
                

                elif count_4 == 4 and ship_name == 'Battleship':
                    if self.ai_ships[1][3]:
                        ship_image = self.ship_images['Battleship']['horizontal']
                    else:
                        ship_image = self.ship_images['Battleship']['vertical']
                    self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))
                
                elif count_5 == 5 and ship_name == 'Aircraft Carrier':
                    if self.ai_ships[0][3]:
                        ship_image = self.ship_images['Aircraft Carrier']['horizontal']
                    else:
                        ship_image = self.ship_images['Aircraft Carrier']['vertical']
                    self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

        # Draw the current ship being placed
        if current_ship_info and ship_pos:
            row, col = ship_pos
            ship_name, ship_size, _ = current_ship_info
            ship_image = self.ship_images[ship_name]['horizontal' if horizontal else 'vertical']

            if self.can_place_ship(grid, row, col, ship_size, horizontal):
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            overlay = pygame.Surface((ship_size * self.settings.cell_size, self.settings.cell_size) if horizontal else (self.settings.cell_size, ship_size * self.settings.cell_size), pygame.SRCALPHA)
            overlay.fill((*color, 128))  # Add some transparency

            if horizontal:
                self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))
                self.screen.blit(overlay, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))
            else:
                self.screen.blit(ship_image, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))
                self.screen.blit(overlay, (start_x + col * self.settings.cell_size, start_y + row * self.settings.cell_size))

        # Draw the text at bottom center of each grid
        self.screen.blit(self.text1, (self.settings.player_grid_start_x + self.settings.grid_size * self.settings.cell_size // 2 - 40, self.settings.player_grid_start_y + self.settings.grid_size * self.settings.cell_size + 10))
        self.screen.blit(self.text2, (self.settings.ai_grid_start_x + self.settings.grid_size * self.settings.cell_size // 2 - 40, self.settings.ai_grid_start_y + self.settings.grid_size * self.settings.cell_size + 10))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        current_ship = self.ships[self.current_ship_index] if self.current_ship_index < len(self.ships) else None
        cell = self.get_cell(pygame.mouse.get_pos(), self.settings.player_grid_start_x, self.settings.player_grid_start_y)
        self.draw_grid(self.settings.player_grid_start_x, self.settings.player_grid_start_y, self.player_grid, self.player_ships, True, current_ship, cell, self.placing_horizontal)
        self.draw_grid(self.settings.ai_grid_start_x, self.settings.ai_grid_start_y, self.ai_grid, self.ai_ships, False)

        if not self.game_started:
            pygame.draw.rect(self.screen, (0, 255, 0) if self.current_ship_index >= len(self.ships) else (255, 0, 0), self.start_button)
            self.screen.blit(self.button_text, (self.settings.screen_width // 2 - 40, self.settings.screen_height - 45))