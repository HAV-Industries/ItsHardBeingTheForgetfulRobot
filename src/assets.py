import pygame
import os


class AssetManager:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(__file__), "img")
        self.background = None
        self.scaled_background = None
        self.last_grid_size = (0, 0)  # Changed from last_size
        self.grass_texture = None
        self.grass_scale = 20  # Scale factor for grass texture
        self.load_assets()

    def load_assets(self):
        # Load background tile
        bg_path = os.path.join(self.assets_dir, "robotfarm_bg1.png")
        self.background = pygame.image.load(bg_path).convert()
        # Store original background for scaling
        self.original_background = self.background
        # Load and scale grass texture
        grass_path = os.path.join(self.assets_dir, "grass.png")
        original_grass = pygame.image.load(grass_path).convert()
        original_size = original_grass.get_size()
        scaled_size = (
            original_size[0] * self.grass_scale,
            original_size[1] * self.grass_scale,
        )
        self.grass_texture = pygame.transform.scale(original_grass, scaled_size)

    def render_grass_sides(
        self, screen, center_x, center_width, window_width, window_height
    ):
        # Get grass tile size
        tile_width = self.grass_texture.get_width()
        tile_height = self.grass_texture.get_height()

        # Calculate areas to fill
        left_area_width = center_x
        right_area_width = window_width - (center_x + center_width)

        # Fill left side
        for y in range(0, window_height, tile_height):
            for x in range(0, left_area_width, tile_width):
                screen.blit(self.grass_texture, (x, y))

        # Fill right side
        right_start = center_x + center_width
        for y in range(0, window_height, tile_height):
            for x in range(right_start, window_width, tile_width):
                screen.blit(self.grass_texture, (x, y))

    def render_background(self, screen, x, y, width, height, padding=16):
        # Draw grass texture first
        self.render_grass_sides(
            screen,
            x - padding,
            width + (padding * 2),
            screen.get_width(),
            screen.get_height(),
        )

        # Scale background to grid size plus padding on each side
        scaled_width = width + (padding * 2)
        scaled_height = height + (padding * 2)

        # Adjust position to account for padding
        padded_x = x - padding
        padded_y = y - padding

        # Only rescale if grid size changed
        if (scaled_width, scaled_height) != self.last_grid_size:
            self.scaled_background = pygame.transform.scale(
                self.original_background, (scaled_width, scaled_height)
            )
            self.last_grid_size = (scaled_width, scaled_height)

        # Draw the scaled background at padded position
        screen.blit(self.scaled_background, (padded_x, padded_y))
