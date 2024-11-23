import pygame
from assets import AssetManager
import random

# Colors
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)  # Darker brown for instructions panel
WHITE = (255, 255, 255)
BUTTON_COLOR = (160, 82, 45)  # Brown button color
BUTTON_HOVER = (185, 100, 55)  # Lighter brown for hover


class Game:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.grid_size = 9
        self.min_cell_size = 80
        self.assets = AssetManager()
        self.bg_padding = 67
        self.window_padding = 150
        self.panel_margin = 20  # Margin for the right panel
        self.font = pygame.font.Font(None, 36)
        self.instructions = []  # List to store movement instructions
        self.button_size = 40
        self.clear_button_size = 30
        self.instruction_rects = []  # Store rectangles for instruction text

        # Initialize grid contents
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.initialize_crops()

    def initialize_crops(self):
        # Place random crops in about 1/3 of the grid spaces
        crop_types = ["carrot", "potato", "wheat"]
        cells_to_fill = (self.grid_size * self.grid_size) // 3

        for _ in range(cells_to_fill):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid[y][x] is None:  # Only fill empty cells
                self.grid[y][x] = random.choice(
                    crop_types
                )  # Just store the crop type string

    def get_cell_size(self):
        width_based = (self.window_width - self.window_padding) // self.grid_size
        height_based = (self.window_height - self.window_padding) // self.grid_size
        return max(min(width_based, height_based), self.min_cell_size)

    def create_dpad_buttons(self, panel_x, panel_y, panel_width):
        center_x = panel_x + panel_width // 2
        center_y = panel_y + 170  # Moved DPAD down from 150 to 170

        # Create button rectangles
        self.buttons = {
            "up": pygame.Rect(
                center_x - self.button_size // 2,
                center_y - self.button_size * 1.2,
                self.button_size,
                self.button_size,
            ),
            "down": pygame.Rect(
                center_x - self.button_size // 2,
                center_y + self.button_size * 0.2,
                self.button_size,
                self.button_size,
            ),
            "left": pygame.Rect(
                center_x - self.button_size * 1.7,
                center_y - self.button_size // 2,
                self.button_size,
                self.button_size,
            ),
            "right": pygame.Rect(
                center_x + self.button_size * 0.7,
                center_y - self.button_size // 2,
                self.button_size,
                self.button_size,
            ),
            "harvest": pygame.Rect(
                center_x - self.button_size // 2,
                center_y - self.button_size // 2,
                self.button_size,
                self.button_size,
            ),
        }

    def handle_button_click(self, pos):
        # Check instruction clear button first
        if hasattr(self, "clear_button_rect") and self.clear_button_rect.collidepoint(
            pos
        ):
            self.instructions = []
            return True

        # Check instruction clicks
        for i, rect in enumerate(self.instruction_rects):
            if rect.collidepoint(pos):
                visible_index = i
                actual_index = len(self.instructions) - len(self.instructions[-8:]) + i
                if 0 <= actual_index < len(self.instructions):
                    self.instructions.pop(actual_index)
                return True

        # Check D-pad buttons
        for action, button in self.buttons.items():
            if button.collidepoint(pos):
                self.instructions.append(action)
                return True
        return False

    def draw(self, screen):
        # Calculate grid dimensions
        cell_size = self.get_cell_size()
        grid_pixel_size = self.grid_size * cell_size

        # Center coordinates for grid
        start_x = 40  # Adjust left margin since editor is gone
        start_y = (self.window_height - grid_pixel_size) // 2

        # Draw scaled background
        self.assets.render_background(
            screen,
            start_x,
            start_y,
            grid_pixel_size,
            grid_pixel_size,
            self.bg_padding,
            0,  # No editor width needed
        )

        # Draw grid lines
        for i in range(self.grid_size + 1):
            # Vertical lines
            pygame.draw.line(
                screen,
                BLACK,
                (start_x + i * cell_size, start_y),
                (start_x + i * cell_size, start_y + grid_pixel_size),
                2,
            )
            # Horizontal lines
            pygame.draw.line(
                screen,
                BLACK,
                (start_x, start_y + i * cell_size),
                (start_x + grid_pixel_size, start_y + i * cell_size),
                2,
            )

        # Draw crops in grid (simplified)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x]:
                    crop_type = self.grid[y][x]  # Just the crop type string
                    crop_sprite = self.assets.get_crop_sprite(crop_type)
                    if crop_sprite:
                        sprite_x = (
                            start_x
                            + (x * cell_size)
                            + (cell_size - crop_sprite.get_width()) // 2
                        )
                        sprite_y = (
                            start_y
                            + (y * cell_size)
                            + (cell_size - crop_sprite.get_height()) // 2
                        )
                        screen.blit(crop_sprite, (sprite_x, sprite_y))

        # Draw right panel
        panel_width = (
            self.window_width - (start_x + grid_pixel_size) - (self.panel_margin * 2)
        )
        panel_height = self.window_height - (self.panel_margin * 2)
        panel_x = start_x + grid_pixel_size + self.panel_margin
        panel_y = self.panel_margin

        pygame.draw.rect(
            screen,
            BROWN,
            (panel_x, panel_y, panel_width, panel_height),
            border_radius=10,
        )

        # Create and draw D-pad buttons
        self.create_dpad_buttons(panel_x, panel_y, panel_width)

        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for action, button in self.buttons.items():
            color = BUTTON_HOVER if button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button, border_radius=5)

            # Draw button labels
            text = self.font.render(action[0].upper(), True, WHITE)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

        # Draw instructions panel
        instructions_width = panel_width - 20
        instructions_height = panel_height // 3
        instructions_x = panel_x + 10
        instructions_y = panel_y + panel_height - instructions_height - 10

        # Draw instructions background
        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (instructions_x, instructions_y, instructions_width, instructions_height),
            border_radius=8,
        )

        # Draw clear button
        self.clear_button_rect = pygame.Rect(
            instructions_x + instructions_width - self.clear_button_size - 5,
            instructions_y + 5,
            self.clear_button_size,
            self.clear_button_size,
        )
        pygame.draw.rect(screen, BUTTON_COLOR, self.clear_button_rect, border_radius=5)
        clear_text = self.font.render("X", True, WHITE)
        clear_text_rect = clear_text.get_rect(center=self.clear_button_rect.center)
        screen.blit(clear_text, clear_text_rect)

        # Reset instruction rectangles list
        self.instruction_rects = []

        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Draw instructions list with numbers continuing from total count
        instruction_y = instructions_y + 10
        visible_instructions = self.instructions[-8:]  # Get last 8 for display
        start_number = max(len(self.instructions) - len(visible_instructions), 0)

        for i, instruction in enumerate(visible_instructions):
            number = start_number + i + 1  # Ensure numbering starts correctly
            text = self.font.render(f"{number}. {instruction}", True, WHITE)
            text_rect = text.get_rect(x=instructions_x + 10, y=instruction_y)

            # Add hover effect
            if text_rect.collidepoint(mouse_pos):
                hover_color = tuple(max(c - 30, 0) for c in WHITE)  # Slightly darker
                text = self.font.render(f"{number}. {instruction}", True, hover_color)

            screen.blit(text, text_rect)

            # Store rectangle for click detection
            self.instruction_rects.append(text_rect)
            instruction_y += 30

        # Draw robot at bottom left of grid
        robot_sprite = self.assets.get_robot_sprite()
        if robot_sprite:
            robot_x = start_x + cell_size // 2 - robot_sprite.get_width() // 2
            robot_y = start_y + grid_pixel_size - robot_sprite.get_height() - 10
            screen.blit(robot_sprite, (robot_x, robot_y))
