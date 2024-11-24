import pygame
import os


class AssetManager:
    def __init__(self):
        self.assets_dir = os.path.join(os.path.dirname(__file__), "img")
        self.background = None
        self.scaled_background = None
        self.last_grid_size = (0, 0)
        self.grass_texture = None
        self.grass_scale = 20
        self.crop_sprites = {}
        self.crop_scales = {
            "carrot": (50, 50),
            "potato": (50, 50),
            "wheat": (80, 80),
        }
        self.robot_sprite = None
        self.load_assets()
        self.load_crop_sprites()

    def load_assets(self):

        bg_path = os.path.join(self.assets_dir, "robotfarm_bg1.png")
        self.background = pygame.image.load(bg_path).convert()

        self.original_background = self.background

        grass_path = os.path.join(self.assets_dir, "grass.png")
        original_grass = pygame.image.load(grass_path).convert()
        original_size = original_grass.get_size()
        scaled_size = (
            original_size[0] * self.grass_scale,
            original_size[1] * self.grass_scale,
        )
        self.grass_texture = pygame.transform.scale(original_grass, scaled_size)

        robot_path = os.path.join(self.assets_dir, "robot.png")
        try:
            self.robot_sprite = pygame.image.load(robot_path).convert_alpha()
            self.robot_sprite = pygame.transform.scale(self.robot_sprite, (60, 60))
        except pygame.error:
            print(f"Could not load robot sprite: {robot_path}")
            self.robot_sprite = None

        collect_path = os.path.join(self.assets_dir, "../", "sfx", "collect.mp3")
        try:
            self.collect_sound = pygame.mixer.Sound(collect_path)
        except pygame.error:
            print(f"Could not load collect sound: {collect_path}")
            self.collect_sound = None

        self.weed_sprite = pygame.image.load(
            os.path.join(self.assets_dir, "weeds", "weeds00.png")
        ).convert_alpha()
        self.weed_sprite = pygame.transform.scale(self.weed_sprite, (40, 40))

    def load_crop_sprites(self):
        crops = {
            "carrot": "carrot/sprite_carrot0.png",
            "potato": "potato/sprite_potato0.png",
            "wheat": "wheat/sprite_wheat0.png",
        }

        for crop_name, sprite_path in crops.items():
            full_path = os.path.join(self.assets_dir, sprite_path)
            try:
                sprite = pygame.image.load(full_path).convert_alpha()

                scale = self.crop_scales.get(crop_name, (50, 50))
                sprite = pygame.transform.scale(sprite, scale)
                self.crop_sprites[crop_name] = sprite
            except pygame.error:
                print(f"Could not load sprite: {full_path}")
                self.crop_sprites[crop_name] = None

    def get_crop_sprite(self, crop_type):
        return self.crop_sprites.get(crop_type)

    def get_robot_sprite(self):
        return self.robot_sprite

    def get_collect_sound(self):
        return self.collect_sound

    def render_grass_sides(
        self,
        screen,
        center_x,
        center_width,
        window_width,
        window_height,
        editor_width=0,
    ):

        tile_width = self.grass_texture.get_width()
        tile_height = self.grass_texture.get_height()

        left_area_width = center_x
        right_area_width = window_width - (center_x + center_width)

        right_start = center_x + center_width
        for y in range(0, window_height, tile_height):
            for x in range(right_start, window_width, tile_width):
                screen.blit(self.grass_texture, (x, y))

    def render_background(
        self, screen, x, y, width, height, padding=16, editor_width=0
    ):

        self.render_grass_sides(
            screen,
            x - padding,
            width + (padding * 2),
            screen.get_width(),
            screen.get_height(),
            editor_width,
        )

        scaled_width = width + (padding * 2)
        scaled_height = height + (padding * 2)

        padded_x = x - padding
        padded_y = y - padding

        if (scaled_width, scaled_height) != self.last_grid_size:
            self.scaled_background = pygame.transform.scale(
                self.original_background, (scaled_width, scaled_height)
            )
            self.last_grid_size = (scaled_width, scaled_height)

        screen.blit(self.scaled_background, (padded_x, padded_y))
