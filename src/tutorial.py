import pygame
import os


BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)


items = [
    "You are a robot",
    "You forget stuff",
    "You have a time limit",
    "You have to collect crops",
    "You can't collect too many crops",
    "You can't collect too few crops",
    "You have to use buttons to write commands to program yourself to collect crops (keyboard shortcuts: arrow keys / spacebar also work)",
    "Use the run button to do your actions",
    "Use the reset button to erase all of your code",
    "To delete an individual command, click on it",
    "If you write too many commands, you will forget what you wrote at the start",
    "You win once you get enough crops in 20 seconds",
]


class Tutorial:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.font = pygame.font.Font(
            "./src/font/Press_Start_2P,Space_Mono/Press_Start_2P/PressStart2P-Regular.ttf",
            17,
        )
        self.background = self.load_background()
        self.current_item_index = 0

    def load_background(self):
        """Load and scale the background image."""
        bg_path = os.path.join(os.path.dirname(__file__), "img", "title_background.png")
        background = pygame.image.load(bg_path)
        return pygame.transform.scale(
            background, (self.window_width, self.window_height)
        )

    def draw(self, screen):
        """Draw the current instruction and 'Next' button."""

        screen.blit(self.background, (0, 0))

        instruction = items[self.current_item_index]
        instruction_surface = self.font.render(instruction, True, DARK_GRAY)
        instruction_rect = instruction_surface.get_rect(
            center=(self.window_width // 2, 200)
        )
        screen.blit(instruction_surface, instruction_rect)

        button_width, button_height = 200, 50
        button_x = (self.window_width - button_width) // 2
        button_y = 350
        next_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        mouse_pos = pygame.mouse.get_pos()
        button_hover = next_button_rect.collidepoint(mouse_pos)

        pygame.draw.rect(
            screen,
            GRAY if button_hover else LIGHT_GRAY,
            next_button_rect,
            border_radius=10,
        )

        button_text = "Next" if self.current_item_index < len(items) - 1 else "Finish"
        button_surface = self.font.render(button_text, True, BLACK)
        button_rect_text = button_surface.get_rect(center=next_button_rect.center)
        screen.blit(button_surface, button_rect_text)

        if button_hover and pygame.mouse.get_pressed()[0]:
            if self.current_item_index < len(items) - 1:
                self.current_item_index += 1
            else:
                return
