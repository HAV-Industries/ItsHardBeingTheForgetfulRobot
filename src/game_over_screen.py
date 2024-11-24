import pygame


class GameOverScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # Fill screen with black
        screen.fill((0, 0, 0))

        # Draw "Game Over" text
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        screen.blit(game_over_text, text_rect)

        # Draw "Try Again" button
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.center = (self.window_width // 2, self.window_height // 2 + 100)
        pygame.draw.rect(screen, (128, 128, 128), button_rect)

        try_again_text = self.button_font.render("Try Again", True, (255, 255, 255))
        text_rect = try_again_text.get_rect(center=button_rect.center)
        screen.blit(try_again_text, text_rect)

        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if button_rect.collidepoint(mouse_pos) and mouse_clicked:
            return True
        return False
