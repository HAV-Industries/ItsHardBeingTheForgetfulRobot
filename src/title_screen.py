import pygame
import os
from tutorial import Tutorial

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)


class TitleScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(
            "./src/font/Press_Start_2P,Space_Mono/Press_Start_2P/PressStart2P-Regular.ttf",
            17,
        )
        # Load background image
        bg_path = os.path.join(os.path.dirname(__file__), "img", "title_background.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(
            self.background, (window_width, window_height)
        )

    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))

        # Draw title
        title = "It's Hard Being the Forgetful Robot"

        # Check if "How to Play" button is clicked

        title_surface = self.font.render(title, True, DARK_GRAY)
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 200))
        screen.blit(title_surface, title_rect)

        # Draw button
        button_width = 200
        button_height = 50
        button_x = (self.window_width - button_width) // 2
        button_y = 350
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Check mouse hover
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)

        # Draw button with hover effect
        pygame.draw.rect(
            screen, GRAY if button_hover else LIGHT_GRAY, button_rect, border_radius=10
        )

        # Draw button text
        button_text = "Start Game"
        text_surface = self.font.render(button_text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Draw second button
        button2_width = 200
        button2_height = 50
        button2_x = (self.window_width - button2_width) // 2
        button2_y = 420
        button2_rect = pygame.Rect(button2_x, button2_y, button2_width, button2_height)

        # Check mouse hover for second button
        button2_hover = button2_rect.collidepoint(mouse_pos)

        # Draw second button with hover effect
        pygame.draw.rect(
            screen,
            GRAY if button2_hover else LIGHT_GRAY,
            button2_rect,
            border_radius=10,
        )

        # Draw second button text
        button2_text = "How to Play"
        text2_surface = self.font.render(button2_text, True, BLACK)
        text2_rect = text2_surface.get_rect(center=button2_rect.center)
        screen.blit(text2_surface, text2_rect)

        if button2_hover and pygame.mouse.get_pressed()[0]:
            Tutorial(self.window_width, self.window_height).draw(screen)
        # Return True if either button is clicked
        return (button_hover and pygame.mouse.get_pressed()[0]) or (
            button2_hover and pygame.mouse.get_pressed()[0]
        )
