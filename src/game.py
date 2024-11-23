import pygame
from assets import AssetManager

# Colors
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)  # Add brown color


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
