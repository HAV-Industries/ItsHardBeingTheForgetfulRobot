import pygame
from assets import AssetManager
import random

# Colors
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)  # Darker brown for instructions panel
WHITE = (255, 255, 255)


class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = 9
        self.min_cell_size = 80
        self.assets = AssetManager()
        self.bg_padding = 67
        self.window_padding = 150
        self.panel_margin = 20  # Margin for the right panel
        self.font = pygame.font.Font(None, 36)
        self.stage = 1  # Add stage variable
        self.instructions = []  # List to store movement instructions

        # Initialize grid contents
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.initialize_crops()

    def initialize_crops(self):
        # Place random crops in about 1/3 of the grid spaces
        crop_types = ["carrot", "potato", "wheat"]
        cells_to_fill = (self.grid_size * self.grid_size) // 3

        for _ in range(cells_to_fill):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid[y][x] is None:  # Only fill empty cells
                self.grid[y][x] = random.choice(
                    crop_types
                )  # Just store the crop type string

    def get_cell_size(self):
        width_based = (self.window_width - self.window_padding) // self.grid_size
        height_based = (self.window_height - self.window_padding) // self.grid_size
        return max(min(width_based, height_based), self.min_cell_size)

    def draw(self, screen):
        # Calculate grid dimensions
        cell_size = self.get_cell_size()
        grid_pixel_size = self.grid_size * cell_size

        # Center coordinates for grid
        start_x = 40  # Adjust left margin since editor is gone
        start_y = (self.window_height - grid_pixel_size) // 2

        # Draw scaled background
        self.assets.render_background(
            screen,
            start_x,
            start_y,
            grid_pixel_size,
            grid_pixel_size,
            self.bg_padding,
            0,  # No editor width needed
        )

        # Draw grid lines
        for i in range(self.grid_size + 1):
            # Vertical lines
            pygame.draw.line(
                screen,
                BLACK,
                (start_x + i * cell_size, start_y),
                (start_x + i * cell_size, start_y + grid_pixel_size),
                2,
            )
            # Horizontal lines
            pygame.draw.line(
                screen,
                BLACK,
                (start_x, start_y + i * cell_size),
                (start_x + grid_pixel_size, start_y + i * cell_size),
                2,
            )

        # Draw crops in grid (simplified)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x]:
                    crop_type = self.grid[y][x]  # Just the crop type string
                    crop_sprite = self.assets.get_crop_sprite(crop_type)
                    if crop_sprite:
                        sprite_x = (
                            start_x
                            + (x * cell_size)
                            + (cell_size - crop_sprite.get_width()) // 2
                        )
                        sprite_y = (
                            start_y
                            + (y * cell_size)
                            + (cell_size - crop_sprite.get_height()) // 2
                        )
                        screen.blit(crop_sprite, (sprite_x, sprite_y))

        # Draw right panel
        panel_width = (
            self.window_width - (start_x + grid_pixel_size) - (self.panel_margin * 2)
        )
        panel_height = self.window_height - (self.panel_margin * 2)
        panel_x = start_x + grid_pixel_size + self.panel_margin
        panel_y = self.panel_margin

        pygame.draw.rect(
            screen,
            BROWN,
            (panel_x, panel_y, panel_width, panel_height),
            border_radius=10,
        )

        # Draw instructions panel
        instructions_width = panel_width - 20  # Slightly smaller than main panel
        instructions_height = panel_height // 3  # One third of main panel
        instructions_x = panel_x + 10
        instructions_y = panel_y + panel_height - instructions_height - 10

        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (instructions_x, instructions_y, instructions_width, instructions_height),
            border_radius=8,
        )

        # Draw robot at bottom left of grid
        robot_sprite = self.assets.get_robot_sprite()
        if robot_sprite:
            robot_x = start_x + cell_size // 2 - robot_sprite.get_width() // 2
            robot_y = start_y + grid_pixel_size - robot_sprite.get_height() - 10
            screen.blit(robot_sprite, (robot_x, robot_y))

        # Add stage counter text
        stage_text = f"Stage {self.stage}"
        text_surface = self.font.render(stage_text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = panel_x + panel_width // 2
        text_rect.top = panel_y + 20
        screen.blit(text_surface, text_rect)
