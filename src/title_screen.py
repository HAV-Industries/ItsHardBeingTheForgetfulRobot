import pygame

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)


class TitleScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 40)

    def draw(self, screen):
        # Draw title
        title = "The Robot has Taken Over!"
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

        # Return True if button is clicked
        return button_hover and pygame.mouse.get_pressed()[0]
