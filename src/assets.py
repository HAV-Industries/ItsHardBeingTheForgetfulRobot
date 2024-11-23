import pygame
import os


class AssetManager:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(__file__), "img")
        self.background = None
        self.scaled_background = None
        self.last_grid_size = (0, 0)  # Changed from last_size
        self.load_assets()

    def load_assets(self):
        # Load background tile
        bg_path = os.path.join(self.assets_dir, "robotfarm_bg1.png")
        self.background = pygame.image.load(bg_path).convert()
        # Store original background for scaling
        self.original_background = self.background

    def render_background(self, screen, x, y, width, height, padding=16):
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
