"""
TODO:
Currently the robot can run more than once. Make it so once you run, that's it and the run button is disabled until you reset.
Add tutorial + the help menu
"""

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
        pygame.display.set_caption(
            "It's Hard Being the Forgetful Robot | Es Difícil Ser el Robot Olvidadizo"
        )

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
                    elif event.key == pygame.K_ESCAPE and self.is_fullscreen:
                        self.toggle_fullscreen()
                    elif event.key in [
                        pygame.K_UP,
                        pygame.K_DOWN,
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                    ]:
                        direction = None
                        if event.key == pygame.K_UP:
                            direction = "up"
                        elif event.key == pygame.K_DOWN:
                            direction = "down"
                        elif event.key == pygame.K_LEFT:
                            direction = "left"
                        elif event.key == pygame.K_RIGHT:
                            direction = "right"
                        if direction:
                            self.game.instructions.append(direction)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_screen == GAME_SCREEN:
                        self.game.handle_button_click(event.pos)

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
    """
    pygame.mixer.music.load(
        os.path.join(os.path.dirname(__file__), "music", "sfx/bg.mp3")
    )
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    """
    game.run()
