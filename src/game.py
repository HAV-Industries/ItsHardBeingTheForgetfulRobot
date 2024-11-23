import pygame

# Colors
BLACK = (0, 0, 0)


class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = 5
        self.min_cell_size = 80

    def get_cell_size(self):
        width_based = (self.window_width - 100) // self.grid_size
        height_based = (self.window_height - 100) // self.grid_size
        return max(min(width_based, height_based), self.min_cell_size)

    def draw(self, screen):
        cell_size = self.get_cell_size()
        grid_pixel_size = self.grid_size * cell_size

        # Center the grid
        start_x = (self.window_width - grid_pixel_size) // 2
        start_y = (self.window_height - grid_pixel_size) // 2

        # Draw grid
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
