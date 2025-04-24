# Import the pygame library
import pygame
import sys

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Grid settings
GRID_SIZE = 20  # Size of each square in the grid (pixels)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200) # Grid lines
GREEN = (0, 150, 0)    # Grass block color
BROWN = (139, 69, 19)  # Dirt block color
BLUE = (0, 0, 200)     # Water block color

# Block types (map color to ID)
BLOCK_TYPES = {
    1: GREEN,  # Grass
    2: BROWN,  # Dirt
    3: BLUE,   # Water
    0: WHITE   # Air (empty) - represents removal
}
# Reverse mapping for convenience (ID to color)
ID_TO_COLOR = {v: k for k, v in BLOCK_TYPES.items()}

# --- Game Setup ---
# Initialize pygame
pygame.init()

# Create the display surface (screen)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 2D Block Placer")

# Create the grid data structure
# A 2D list (list of lists) to store the state of each cell
# 0 represents an empty cell (WHITE)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# --- Current Tool ---
# Start with Grass block selected
current_block_id = 1
print("Controls:")
print(" Left Click: Place selected block")
print(" Right Click: Remove block (set to Air)")
print(" Keys 1, 2, 3: Select Grass, Dirt, Water")
print(" Key 0: Select Eraser (Air)")
print(f"Selected Block: {list(BLOCK_TYPES.keys())[list(BLOCK_TYPES.values()).index(BLOCK_TYPES[current_block_id])]}")


# --- Functions ---
def draw_grid():
    """Draws the grid lines on the screen."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

def draw_blocks():
    """Draws the colored blocks based on the grid data."""
    for y, row in enumerate(grid):
        for x, cell_value in enumerate(row):
            if cell_value != 0: # Only draw if not empty (Air)
                color = BLOCK_TYPES.get(cell_value, WHITE) # Get color from ID
                # Calculate rectangle position and size
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, rect)

def get_grid_pos(mouse_pos):
    """Converts mouse coordinates to grid coordinates."""
    mx, my = mouse_pos
    grid_x = mx // GRID_SIZE
    grid_y = my // GRID_SIZE
    # Ensure coordinates are within grid bounds
    grid_x = max(0, min(grid_x, GRID_WIDTH - 1))
    grid_y = max(0, min(grid_y, GRID_HEIGHT - 1))
    return grid_x, grid_y

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit loop if window is closed

        # Mouse Button Presses
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x, grid_y = get_grid_pos(mouse_pos)

            if event.button == 1: # Left mouse button
                # Place the current block type
                grid[grid_y][grid_x] = current_block_id
                print(f"Placed block {current_block_id} at ({grid_x}, {grid_y})")

            elif event.button == 3: # Right mouse button
                # Remove block (set to 0/Air)
                removed_block = grid[grid_y][grid_x]
                grid[grid_y][grid_x] = 0
                print(f"Removed block {removed_block} at ({grid_x}, {grid_y})")

        # Keyboard Presses for selecting block type
        if event.type == pygame.KEYDOWN:
            new_block_selected = False
            if event.key == pygame.K_1:
                current_block_id = 1 # Grass
                new_block_selected = True
            elif event.key == pygame.K_2:
                current_block_id = 2 # Dirt
                new_block_selected = True
            elif event.key == pygame.K_3:
                current_block_id = 3 # Water
                new_block_selected = True
            elif event.key == pygame.K_0:
                current_block_id = 0 # Air (Eraser)
                new_block_selected = True

            if new_block_selected:
                 block_name = "Eraser" if current_block_id == 0 else list(BLOCK_TYPES.keys())[list(BLOCK_TYPES.values()).index(BLOCK_TYPES[current_block_id])]
                 print(f"Selected Block: {block_name}")


    # --- Drawing ---
    screen.fill(WHITE)   # Fill background with white each frame
    draw_blocks()        # Draw the placed blocks
    draw_grid()          # Draw the grid lines over the blocks

    # --- Update Display ---
    pygame.display.flip() # Update the full screen to show drawn elements

# --- Cleanup ---
pygame.quit()
sys.exit()
