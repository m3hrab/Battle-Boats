import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 10
CELL_SIZE = 30
MARGIN = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Battleship Game')

# Define ship information
ships = [
    ("Aircraft Carrier", 5, 'assets/images/AircraftCarrier.png'),
    ("Battleship", 4, 'assets/images/Rescue.png'),
    ("Cruiser", 3, 'assets/images/Cruiser.png'),
    ("Submarine", 3, 'assets/images/SubMarine.png'),
    ("Destroyer", 2, 'assets/images/Destroyer.png')
]


# Load ship images and create rotated versions for horizontal placement
ship_images = {}
for name, size, image_path in ships:
    image = pygame.image.load(image_path)
    horizontal_image = pygame.transform.scale(image, (size * CELL_SIZE, CELL_SIZE))
    vertical_image = pygame.transform.rotate(horizontal_image, 90)
    ship_images[name] = {'horizontal': horizontal_image, 'vertical': vertical_image}

# Create grid states for the player and AI
player_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
ai_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
player_ships = []

# Helper function to check if a ship can be placed at a given position
def can_place_ship(grid, row, col, size, horizontal):
    if horizontal:
        if col + size > GRID_SIZE:
            return False
        for i in range(size):
            if grid[row][col + i] != 0:
                return False
    else:
        if row + size > GRID_SIZE:
            return False
        for i in range(size):
            if grid[row + i][col] != 0:
                return False
    return True

# Helper function to place a ship on the grid
def place_ship(grid, row, col, size, horizontal):
    if horizontal:
        for i in range(size):
            grid[row][col + i] = 1
    else:
        for i in range(size):
            grid[row + i][col] = 1

def draw_grid(screen, start_x, start_y, grid, player_ships, current_ship_info=None, ship_pos=None, horizontal=True):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(start_x + col * CELL_SIZE, start_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, rect, 1)
            if grid[row][col] == 1:
                pass
    
    for ship_name, ship_size, (row, col), ship_horizontal in player_ships:
        ship_image = ship_images[ship_name]['horizontal' if ship_horizontal else 'vertical']
        screen.blit(ship_image, (start_x + col * CELL_SIZE, start_y + row * CELL_SIZE))

    if current_ship_info and ship_pos:
        row, col = ship_pos
        ship_name, ship_size, _ = current_ship_info
        ship_image = ship_images[ship_name]['horizontal' if horizontal else 'vertical']

        if can_place_ship(grid, row, col, ship_size, horizontal):
            color = GREEN
        else:
            color = RED
        overlay = pygame.Surface((ship_size * CELL_SIZE, CELL_SIZE) if horizontal else (CELL_SIZE, ship_size * CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((*color, 128))  # Add some transparency

        if horizontal:
            screen.blit(ship_image, (start_x + col * CELL_SIZE, start_y + row * CELL_SIZE))
            screen.blit(overlay, (start_x + col * CELL_SIZE, start_y + row * CELL_SIZE))
        else:
            screen.blit(ship_image, (start_x + col * CELL_SIZE, start_y + row * CELL_SIZE))
            screen.blit(overlay, (start_x + col * CELL_SIZE, start_y + row * CELL_SIZE))

def get_cell(mouse_pos, start_x, start_y):
    x, y = mouse_pos
    if start_x <= x < start_x + GRID_SIZE * CELL_SIZE and start_y <= y < start_y + GRID_SIZE * CELL_SIZE:
        col = (x - start_x) // CELL_SIZE
        row = (y - start_y) // CELL_SIZE
        return row, col
    return None

def place_ai_ships():
    for ship_name, ship_size, _ in ships:
        placed = False
        while not placed:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            horizontal = random.choice([True, False])
            if can_place_ship(ai_grid, row, col, ship_size, horizontal):
                place_ship(ai_grid, row, col, ship_size, horizontal)
                placed = True

# Define the starting positions for the player and AI grids
player_grid_start_x, player_grid_start_y = MARGIN, MARGIN
ai_grid_start_x, ai_grid_start_y = SCREEN_WIDTH - MARGIN - GRID_SIZE * CELL_SIZE, MARGIN

# Variables for ship placement
current_ship_index = 0
placing_horizontal = True

# Place AI ships
place_ai_ships()

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_cell(mouse_pos, player_grid_start_x, player_grid_start_y)
            if cell and current_ship_index < len(ships):
                row, col = cell
                ship_name, ship_size, _ = ships[current_ship_index]
                if can_place_ship(player_grid, row, col, ship_size, placing_horizontal):
                    place_ship(player_grid, row, col, ship_size, placing_horizontal)
                    player_ships.append((ship_name, ship_size, (row, col), placing_horizontal))
                    current_ship_index += 1

                if current_ship_index == len(ships):
                    print("All ships placed!")
                    print("Player ships:")
                    for row in player_grid:
                        print(row)

                    print("\nAI ships:")
                    for row in ai_grid:
                        print(row)


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                placing_horizontal = not placing_horizontal

            # Reset the game
            elif event.key == pygame.K_p:
                player_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                ai_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                player_ships = []
                current_ship_index = 0
                place_ai_ships()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player and AI grids
    current_ship = ships[current_ship_index] if current_ship_index < len(ships) else None
    cell = get_cell(mouse_pos, player_grid_start_x, player_grid_start_y)
    draw_grid(screen, player_grid_start_x, player_grid_start_y, player_grid, player_ships, current_ship, cell, placing_horizontal)
    draw_grid(screen, ai_grid_start_x, ai_grid_start_y, ai_grid, [])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
