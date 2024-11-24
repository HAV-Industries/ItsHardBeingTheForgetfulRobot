"""
TODO:
Add tutorial + the help menu
"""

import pygame
import sys
import os
from title_screen import TitleScreen
from game import Game
from game_over_screen import *
from game_win_screen import GameWinScreen
from tutorial import Tutorial
import time


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


TITLE_SCREEN = 0
GAME_SCREEN = 1
GAME_OVER = 2
GAME_WIN = 3
TUTORIAL_SCREEN = 4


class GameController:
    def __init__(self):
        pygame.init()

        icon_path = os.path.join(os.path.dirname(__file__), "img", "icon.png")
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("It's Hard Being the Forgetful Robot")

        self.is_fullscreen = False
        self.current_screen = TITLE_SCREEN

        self.title_screen = TitleScreen(self.window_width, self.window_height)
        self.game = Game(self.window_width, self.window_height)
        self.game_over_screen = GameOverScreen(self.window_width, self.window_height)
        self.game_win_screen = GameWinScreen(self.window_width, self.window_height)
        self.tutorial = Tutorial(self.window_width, self.window_height)
        self.GAME_OVER = 2

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

        self.title_screen = TitleScreen(self.window_width, self.window_height)
        self.game = Game(self.window_width, self.window_height)

    def run(self):
        while True:

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
                        pygame.K_SPACE,
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
                        elif event.key == pygame.K_SPACE:
                            direction = "harvest"
                        if direction:
                            self.game.instructions.append(direction)
                            self.game.instructions = self.game.instructions[-50:]
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_screen == GAME_SCREEN:
                        self.game.handle_button_click(event.pos)
                    elif self.current_screen == TUTORIAL_SCREEN:

                        pass

            self.screen.fill((255, 255, 255))

            if self.current_screen == TITLE_SCREEN:
                result = self.title_screen.draw(self.screen)
                if isinstance(result, str):
                    if result == "GAME_SCREEN":
                        self.current_screen = GAME_SCREEN
                    elif result == "TUTORIAL_SCREEN":
                        self.current_screen = TUTORIAL_SCREEN
            elif self.current_screen == GAME_SCREEN:
                self.game.draw(self.screen)
                if self.game.game_over:
                    self.current_screen = GAME_OVER
                elif self.game.game_win:
                    self.current_screen = GAME_WIN
            elif self.current_screen == GAME_OVER:
                if self.game_over_screen.draw(self.screen):

                    self.game = Game(self.window_width, self.window_height)
                    self.current_screen = GAME_SCREEN
            elif self.current_screen == GAME_WIN:
                if self.game_win_screen.draw(self.screen):

                    self.game = Game(self.window_width, self.window_height)
                    self.current_screen = GAME_SCREEN
            elif self.current_screen == TUTORIAL_SCREEN:
                result = self.tutorial.draw(self.screen)
                if result == "DONE":
                    self.current_screen = TITLE_SCREEN

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameController()

    music_path = os.path.join(os.path.dirname(__file__), "sfx", "bg.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

    game.run()
