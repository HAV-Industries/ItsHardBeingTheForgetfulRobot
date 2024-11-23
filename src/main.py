import pygame
import sys
from title_screen import TitleScreen
from game import Game

# Constants
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1


class GameController:
    def __init__(self):
        pygame.init()
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE,  # Add resizable flag
        )
        pygame.display.set_caption("The Robot has Taken Over!")

        self.is_fullscreen = False
        self.current_screen = TITLE_SCREEN

        # Initialize screens
        self.title_screen = TitleScreen(self.window_width, self.window_height)
        self.game = Game(self.window_width, self.window_height)

        self.clock = pygame.time.Clock()

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Store current window position
            x, y = pygame.display.get_window_pos()
            screen_info = pygame.display.Info()
            self.window_width = screen_info.current_w
            self.window_height = screen_info.current_h
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height), pygame.FULLSCREEN
            )
        else:
            # Return to windowed mode at the same position
            self.window_width = WINDOW_WIDTH
            self.window_height = WINDOW_HEIGHT
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height), pygame.RESIZABLE
            )

        # Update screen dimensions for both game states
        self.title_screen = TitleScreen(self.window_width, self.window_height)
        self.game = Game(self.window_width, self.window_height)

    def run(self):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE and self.is_fullscreen:
                        self.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize events
                    if not self.is_fullscreen:
                        self.window_width = event.w
                        self.window_height = event.h
                        self.screen = pygame.display.set_mode(
                            (self.window_width, self.window_height), pygame.RESIZABLE
                        )
                        # Update screen dimensions for both game states
                        self.title_screen = TitleScreen(
                            self.window_width, self.window_height
                        )
                        self.game = Game(self.window_width, self.window_height)
                elif event.type == pygame.WINDOWMAXIMIZED:
                    # Handle window maximize event
                    screen_info = pygame.display.Info()
                    self.window_width = screen_info.current_w
                    self.window_height = screen_info.current_h
                    self.title_screen = TitleScreen(
                        self.window_width, self.window_height
                    )
                    self.game = Game(self.window_width, self.window_height)

            # Clear screen
            self.screen.fill((255, 255, 255))

            # Update and draw current screen
            if self.current_screen == TITLE_SCREEN:
                if self.title_screen.draw(self.screen):
                    self.current_screen = GAME_SCREEN
            elif self.current_screen == GAME_SCREEN:
                self.game.draw(self.screen)

            # Update display
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameController()
    game.run()
