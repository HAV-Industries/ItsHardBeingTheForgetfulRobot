import pygame
import os
from tutorial import Tutorial


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
BROWN = (149, 79, 29)
LIGHT_BROWN = (185, 100, 55)


class TitleScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(
            "./src/font/Press_Start_2P,Space_Mono/Press_Start_2P/PressStart2P-Regular.ttf",
            17,
        )

        self.font2 = pygame.font.Font(
            "./src/font/Press_Start_2P,Space_Mono/Press_Start_2P/PressStart2P-Regular.ttf",
            25,
        )

        bg_path = os.path.join(os.path.dirname(__file__), "img", "title_background.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(
            self.background, (window_width, window_height)
        )

    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        title = "It's Hard Being the Forgetful Robot"
        title_surface = self.font2.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 200))

        padding = 20
        box_rect = pygame.Rect(
            title_rect.left - padding,
            title_rect.top - padding,
            title_rect.width + (padding * 2),
            title_rect.height + (padding * 2),
        )
        pygame.draw.rect(screen, LIGHT_BROWN, box_rect, border_radius=10)

        screen.blit(title_surface, title_rect)

        button_width = 200
        button_height = 50
        button_x = (self.window_width - button_width) // 2
        button_y = 350
        start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(
            screen,
            GRAY if start_button_rect.collidepoint(mouse_pos) else LIGHT_GRAY,
            start_button_rect,
            border_radius=10,
        )
        start_text = self.font.render("Start Game", True, BLACK)
        start_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_rect)

        button2_width = 200
        button2_height = 50
        button2_x = (self.window_width - button2_width) // 2
        button2_y = 420
        how_to_play_rect = pygame.Rect(
            button2_x, button2_y, button2_width, button2_height
        )

        pygame.draw.rect(
            screen,
            GRAY if how_to_play_rect.collidepoint(mouse_pos) else LIGHT_GRAY,
            how_to_play_rect,
            border_radius=10,
        )
        how_to_play_text = self.font.render("How to Play", True, BLACK)
        how_to_play_rect_text = how_to_play_text.get_rect(
            center=how_to_play_rect.center
        )
        screen.blit(how_to_play_text, how_to_play_rect_text)

        if start_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return "GAME_SCREEN"
        if how_to_play_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return "TUTORIAL_SCREEN"
