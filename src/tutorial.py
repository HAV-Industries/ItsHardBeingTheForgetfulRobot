import pygame
import os


BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
BROWN = (149, 79, 29)


items = [
    "You are a robot",
    "You forget stuff",
    "You have a time limit (20 seconds)",
    "You have to collect enough crops",
    "You have to use buttons to write commands",
    "Commands program you to collect crops. (Keyboard shortcuts: arrow keys / spacebar also work)",
    "Weeds increase your deviation chance and take your food.",
    "Deviations make your instructions less accurate.",
    "Use the run button to do your instructions",
    "Use the reset button to erase all of your instructions. Or click on individual commands to delete them.",
    "You can only see your last 7 commands. You can't see or change any commands before that.",
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
        self.clicking = False

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
        lines = instruction.split(". ")
        padding = 20
        total_height = sum(self.font.size(line)[1] for line in lines) + padding * (
            len(lines) + 1
        )
        max_width = max(self.font.size(line)[0] for line in lines) + padding * 2

        box_rect = pygame.Rect(
            (self.window_width - max_width) // 2,
            200 - total_height // 2,
            max_width,
            total_height,
        )
        pygame.draw.rect(screen, BROWN, box_rect, border_radius=10)

        y_offset = box_rect.top + padding
        for line in lines:
            instruction_surface = self.font.render(line, True, BLACK)
            instruction_rect = instruction_surface.get_rect(
                center=(self.window_width // 2, y_offset)
            )
            screen.blit(instruction_surface, instruction_rect)
            y_offset += self.font.size(line)[1] + padding

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

        if button_hover and pygame.mouse.get_pressed()[0] and not self.clicking:
            if self.current_item_index < len(items) - 1:
                self.current_item_index += 1
            else:
                return "DONE"
            self.clicking = True
        elif not pygame.mouse.get_pressed()[0]:
            self.clicking = False
