import pygame


class GameWinScreen:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # Fill screen with green
        screen.fill((0, 255, 0))

        # Draw "You Win!" text
        win_text = self.font.render("You Win!", True, (0, 0, 0))
        text_rect = win_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        screen.blit(win_text, text_rect)

        # Draw "Play Again" button
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.center = (self.window_width // 2, self.window_height // 2 + 100)
        pygame.draw.rect(screen, (128, 128, 128), button_rect)

        play_again_text = self.button_font.render("Play Again", True, (255, 255, 255))
        text_rect = play_again_text.get_rect(center=button_rect.center)
        screen.blit(play_again_text, text_rect)

        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if button_rect.collidepoint(mouse_pos) and mouse_clicked:
            return True
        return False
