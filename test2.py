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
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]

# Create grid states for the player and AI
player_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
ai_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

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

def draw_grid(screen, start_x, start_y, grid, ship_size=None, ship_pos=None, horizontal=True):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(start_x + col * CELL_SIZE, start_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLUE, rect, 1)

    if ship_size and ship_pos:
        row, col = ship_pos
        if can_place_ship(grid, row, col, ship_size, horizontal):
            color = YELLOW
        else:
            color = RED
        for i in range(ship_size):
            if horizontal:
                if col + i < GRID_SIZE:
                    rect = pygame.Rect(start_x + (col + i) * CELL_SIZE, start_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, rect)
            else:
                if row + i < GRID_SIZE:
                    rect = pygame.Rect(start_x + col * CELL_SIZE, start_y + (row + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, color, rect)

def get_cell(mouse_pos, start_x, start_y):
    x, y = mouse_pos
    if start_x <= x < start_x + GRID_SIZE * CELL_SIZE and start_y <= y < start_y + GRID_SIZE * CELL_SIZE:
        col = (x - start_x) // CELL_SIZE
        row = (y - start_y) // CELL_SIZE
        return row, col
    return None

def place_ai_ships():
    for ship_name, ship_size in ships:
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
                ship_name, ship_size = ships[current_ship_index]
                if can_place_ship(player_grid, row, col, ship_size, placing_horizontal):
                    place_ship(player_grid, row, col, ship_size, placing_horizontal)
                    current_ship_index += 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                placing_horizontal = not placing_horizontal

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player and AI grids
    current_ship = ships[current_ship_index] if current_ship_index < len(ships) else None
    ship_size = current_ship[1] if current_ship else None
    cell = get_cell(mouse_pos, player_grid_start_x, player_grid_start_y)
    draw_grid(screen, player_grid_start_x, player_grid_start_y, player_grid, ship_size, cell, placing_horizontal)
    draw_grid(screen, ai_grid_start_x, ai_grid_start_y, ai_grid)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
