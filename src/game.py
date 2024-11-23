import pygame
from assets import AssetManager

# Colors
BLACK = (0, 0, 0)


class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = 9
        self.min_cell_size = 80
        self.assets = AssetManager()
        self.bg_padding = 96  # Adjust this value to control background extension

    def get_cell_size(self):
        width_based = (self.window_width - 100) // self.grid_size
        height_based = (self.window_height - 100) // self.grid_size
        return max(min(width_based, height_based), self.min_cell_size)

    def draw(self, screen):
        # Calculate grid dimensions first
        cell_size = self.get_cell_size()
        grid_pixel_size = self.grid_size * cell_size

        # Center coordinates
        start_x = (self.window_width - grid_pixel_size) // 2
        start_y = (self.window_height - grid_pixel_size) // 2

        # Draw scaled background to match grid size plus padding
        self.assets.render_background(
            screen, start_x, start_y, grid_pixel_size, grid_pixel_size, self.bg_padding
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
