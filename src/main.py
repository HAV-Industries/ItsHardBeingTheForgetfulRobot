import pygame
import sys
import os
from title_screen import TitleScreen
from game import Game
import time


# Constants
WINDOW_WIDTH = 1280  # Changed from 1920
WINDOW_HEIGHT = 720  # Changed from 1080

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1


class GameController:
    def __init__(self):
        pygame.init()
        # Set game icon
        icon_path = os.path.join(os.path.dirname(__file__), "img", "icon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        # Remove resizable flag
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
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
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height)
            )

        # Update screen dimensions for both game states
        self.title_screen = TitleScreen(self.window_width, self.window_height)
        self.game = Game(self.window_width, self.window_height)

    def run(self):
        while True:
            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE and self.is_fullscreen:
                        self.toggle_fullscreen()

            # Clear screen
            self.screen.fill((255, 255, 255))

            # Update and draw current screen
            if self.current_screen == TITLE_SCREEN:
                if self.title_screen.draw(self.screen):
                    self.current_screen = GAME_SCREEN
            elif self.current_screen == GAME_SCREEN:
                self.game.draw(self.screen)  # Remove store_events call

            # Update display
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameController()
    game.run()
