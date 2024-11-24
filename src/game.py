import pygame
from assets import AssetManager
import random
import copy  # Added for deep copying the grid
import time
import tutorial
import os

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
        self.font = pygame.font.Font(
            "./src/font/Press_Start_2P,Space_Mono/Press_Start_2P/PressStart2P-Regular.ttf",
            17,
        )
        # self.font = pygame.font.Font(None, 36)

        self.run_button_disabled = False  # Flag to disable run button after running
        self.instructions = []  # List to store movement instructions
        self.food_level = 0  # Initialize food level
        self.robot_position = (
            self.grid_size - 1,
            self.grid_size - 1,
        )  # Start at bottom right
        self.run_button_disabled = False  # Initialize run button state
        self.initial_grid = []  # To store initial grid for reset
        self.is_running = False  # Flag to check if instructions are being executed
        self.current_instruction_index = 0  # To track current instruction
        self.button_size = 40
        self.clear_button_size = 30
        self.instruction_rects = []  # Store rectangles for instruction text
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_active = False
        self.game_time = 20  # Starting time in seconds
        self.game_over = False
        self.deviation_count = 0  # Initialize deviation counter
        self.game_win = False  # Add game win flag
        self.initial_crop_count = 0  # Add this line to track initial number of crops

        self.button_icons = {
            "up": pygame.image.load(
                os.path.join(os.path.dirname(__file__), "img", "arrow-up.png")
            ),
            "down": pygame.image.load(
                os.path.join(os.path.dirname(__file__), "img", "arrow-down.png")
            ),
            "left": pygame.image.load(
                os.path.join(os.path.dirname(__file__), "img", "arrow-left.png")
            ),
            "right": pygame.image.load(
                os.path.join(os.path.dirname(__file__), "img", "arrow-right.png")
            ),
            "harvest": pygame.image.load(
                os.path.join(os.path.dirname(__file__), "img", "basket.png")
            ),
        }
        # Scale icons to fit buttons, with basket being larger
        for key in self.button_icons:
            if key == "harvest":
                self.button_icons[key] = pygame.transform.scale(
                    self.button_icons[key], (40, 40)
                )  # Larger basket
            else:
                self.button_icons[key] = pygame.transform.scale(
                    self.button_icons[key], (30, 30)
                )  # Normal arrows

        # Initialize grid contents
        self.grid = [
            [None for _ in range(self.grid_size)] for _ in range(self.grid_size)
        ]
        self.initialize_crops()
        self.initial_grid = copy.deepcopy(self.grid)  # Store initial grid

        # Create Run and Reset buttons

        # Set spacebar as a shortcut for the harvest button
        self.run_button = pygame.Rect(0, 0, 100, 40)
        self.reset_button = pygame.Rect(0, 0, 100, 40)

    def initialize_crops(self):
        # Ensure at least 1/3 of the grid spaces are occupied by crops
        crop_types = ["carrot", "potato", "wheat", "weed"]  # Include 'weed'
        total_cells = self.grid_size * self.grid_size
        cells_to_fill = total_cells // 3

        positions = [
            (x, y) for x in range(self.grid_size) for y in range(self.grid_size)
        ]
        random.shuffle(positions)
        selected_positions = positions[:cells_to_fill]

        for x, y in selected_positions:
            self.grid[y][x] = random.choice(crop_types)

        # Store the initial number of crops
        self.initial_crop_count = cells_to_fill

    def spawn_weeds(self):
        # Spawn a weed randomly on an empty cell
        empty_cells = [
            (x, y)
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if self.grid[y][x] is None
        ]
        if empty_cells:
            spawn_x, spawn_y = random.choice(empty_cells)
            self.grid[spawn_y][spawn_x] = "weed"

    def get_current_crop_count(self):
        return sum(
            1
            for y in range(self.grid_size)
            for x in range(self.grid_size)
            if self.grid[y][x] is not None
        )

    def get_cell_size(self):
        width_based = (self.window_width - self.window_padding) // self.grid_size
        height_based = (self.window_height - self.window_padding) // self.grid_size
        return max(min(width_based, height_based), self.min_cell_size)

    def create_dpad_buttons(self, panel_x, panel_y, panel_width):
        center_x = panel_x + panel_width // 2
        center_y = panel_y + 350

        # Create button rectangles
        self.buttons = {
            "up": pygame.Rect(
                center_x - self.button_size // 2,
                center_y - self.button_size * 1.67,
                self.button_size,
                self.button_size,
            ),
            "down": pygame.Rect(
                center_x - self.button_size // 2,
                center_y + self.button_size * 0.65,
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
                # Check How to Play button

        # Check D-pad buttons
        for action, button in self.buttons.items():
            if button.collidepoint(pos):
                self.instructions.append(action)
                self.instructions = self.instructions[-50:]
                return True

        # Check Run button
        if self.run_button.collidepoint(pos):
            if not self.is_running and not self.run_button_disabled:
                self.is_running = True
                self.current_instruction_index = 0
                self.run_button_disabled = True
                self.start_time = time.time()  # Start the timer
                self.timer_active = True
            return True

        # Check Reset button
        if self.reset_button.collidepoint(pos):
            self.reset_game()
            self.run_button_disabled = False
            return True

        return False

    def reset_game(self):
        self.grid = copy.deepcopy(self.initial_grid)  # Reset grid to initial state
        self.robot_position = (
            self.grid_size - 1,
            self.grid_size - 1,
        )  # Reset robot position
        self.instructions = []  # Clear instructions
        self.food_level = 0  # Reset food level
        self.is_running = False  # Stop running
        self.current_instruction_index = 0  # Reset instruction index
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_active = False
        self.deviation_count = 0  # Reset deviation count
        self.game_win = False  # Reset game win flag
        self.game_over = False
        self.game_win = False  # Add this line

    def execute_instruction(self, instruction):
        x, y = self.robot_position

        error_chance = len(self.instructions) / 1000
        random_action_taken = False
        if random.random() < error_chance:
            instruction = random.choice(["up", "down", "left", "right", "harvest"])
            self.deviation_count += 1  # Increment deviation count
            random_action_taken = True

        if instruction == "up":
            if y > 0:
                self.robot_position = (x, y - 1)
        elif instruction == "down":
            if y < self.grid_size - 1:
                self.robot_position = (x, y + 1)
        elif instruction == "left":
            if x > 0:
                self.robot_position = (x - 1, y)
        elif instruction == "right":
            if x < self.grid_size - 1:
                self.robot_position = (x + 1, y)
        elif instruction == "harvest" or random_action_taken:
            if random_action_taken:
                # If a random action was taken due to error
                pass
            else:
                # Harvesting action
                pass
            if self.grid[y][x]:
                if self.grid[y][x] == "weed":
                    self.food_level -= 2  # Penalty for encountering weeds
                    self.deviation_count += 1  # Additional penalty
                    # Optionally play a negative sound effect
                else:
                    self.grid[y][x] = None
                    self.food_level += 1
                    # Play collect sound effect without affecting background music
                    collect_sound = self.assets.get_collect_sound()
                    if collect_sound:
                        collect_sound.play()
        time.sleep(0.2)

        # Only spawn a new crop if we're below the initial count
        current_crops = self.get_current_crop_count()
        if current_crops < self.initial_crop_count:
            empty_cells = [
                (x, y)
                for y in range(self.grid_size)
                for x in range(self.grid_size)
                if self.grid[y][x] is None
            ]
            if empty_cells:
                spawn_x, spawn_y = random.choice(empty_cells)
                self.grid[spawn_y][spawn_x] = random.choice(
                    ["carrot", "potato", "wheat", "weed"]  # Include 'weed' in spawn
                )

    def draw_progress_bar(self, screen, x, y, width, height, progress):
        # Draw the background of the progress bar
        pygame.draw.rect(screen, WHITE, (x, y, width, height), border_radius=5)
        # Draw the progress
        inner_width = int(width * progress)
        pygame.draw.rect(
            screen, BUTTON_HOVER, (x, y, inner_width, height), border_radius=5
        )

    def update(self):
        if self.is_running:
            # Execute current instruction
            if len(self.instructions) > 0:  # Only if there are instructions
                instruction = self.instructions[self.current_instruction_index]
                self.execute_instruction(instruction)

                # Move to next instruction, loop back to start if at end
                self.current_instruction_index = (
                    self.current_instruction_index + 1
                ) % len(self.instructions)

            # Check timer
            if self.timer_active:
                current_time = time.time() - self.start_time
                remaining_time = self.game_time - current_time
                if remaining_time <= 0:
                    # Check if food level requirement is met
                    required_food = self.grid_size * self.grid_size // 4
                    if self.food_level < required_food:
                        self.game_over = True
                    else:
                        self.game_win = True  # Trigger win condition
                    self.timer_active = False

            # Spawn weeds every 10 seconds
            if not hasattr(self, "last_weed_spawn"):
                self.last_weed_spawn = time.time()
            elif time.time() - self.last_weed_spawn > 10:
                self.spawn_weeds()
                self.last_weed_spawn = time.time()

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

        # Remove or comment out grid lines drawing
        # for i in range(self.grid_size + 1):
        #     pygame.draw.line(...)
        #     pygame.draw.line(...)

        # Draw crops in grid (including weeds)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x]:
                    crop_type = self.grid[y][x]  # Just the crop type string
                    if crop_type == "weed":
                        sprite = self.assets.weed_sprite
                    else:
                        sprite = self.assets.get_crop_sprite(crop_type)
                    if sprite:
                        sprite_x = (
                            start_x
                            + (x * cell_size)
                            + (cell_size - sprite.get_width()) // 2
                        )
                        sprite_y = (
                            start_y
                            + (y * cell_size)
                            + (cell_size - sprite.get_height()) // 2
                        )

                        # Add offset for wheat sprite
                        if crop_type == "wheat":
                            sprite_y -= (
                                10  # Adjust this value to move wheat up more or less
                            )

                        screen.blit(sprite, (sprite_x, sprite_y))

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

        # Draw buttons with hover effect and icons (replace the text rendering section)
        mouse_pos = pygame.mouse.get_pos()
        for action, button in self.buttons.items():
            # Special background color for harvest button
            if action == "harvest":
                color = (
                    (100, 200, 200)
                    if button.collidepoint(mouse_pos)
                    else (75, 125, 150)
                )  # Green shades
            else:
                color = BUTTON_HOVER if button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button, border_radius=5)

            # Draw icon instead of text
            icon = self.button_icons[action]
            icon_rect = icon.get_rect(center=button.center)
            screen.blit(icon, icon_rect)

        # Draw Run and Reset buttons
        if not self.is_running and not self.run_button_disabled:
            self.run_button.topleft = (panel_x + 10, panel_y + 10)
            pygame.draw.rect(screen, BUTTON_COLOR, self.run_button, border_radius=5)
            run_text = self.font.render("Run", True, WHITE)
            run_text_rect = run_text.get_rect(center=self.run_button.center)
            screen.blit(run_text, run_text_rect)

        self.reset_button.topleft = (panel_x + panel_width - 110, panel_y + 10)
        pygame.draw.rect(screen, BUTTON_COLOR, self.reset_button, border_radius=5)
        reset_text = self.font.render("Reset", True, WHITE)
        reset_text_rect = reset_text.get_rect(center=self.reset_button.center)
        screen.blit(reset_text, reset_text_rect)

        # Draw Food Level counter
        food_text = self.font.render(f"Food Level: {self.food_level}", True, WHITE)
        food_rect = food_text.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 35)
        )
        self.draw_progress_bar(
            screen,
            panel_x + 10,
            panel_y + 55,
            panel_width - 20,
            30,
            self.food_level / (self.grid_size * self.grid_size // 4),  # Reduced quota
        )
        screen.blit(food_text, food_rect)

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
        visible_instructions = self.instructions[-7:]  # Get last 8 for display
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

        # Draw robot at current position
        robot_sprite = self.assets.get_robot_sprite()
        if robot_sprite:
            robot_x = (
                start_x
                + self.robot_position[0] * cell_size
                + (cell_size - robot_sprite.get_width()) // 2
            )
            robot_y = (
                start_y
                + self.robot_position[1] * cell_size
                + (cell_size - robot_sprite.get_height()) // 2
            )
            screen.blit(robot_sprite, (robot_x, robot_y))

        # Draw timer if active
        if self.timer_active:
            remaining_time = max(0, self.game_time - (time.time() - self.start_time))
            timer_text = self.font.render(f"Time: {remaining_time:.1f}s", True, WHITE)
            timer_rect = timer_text.get_rect(
                center=(panel_x + panel_width // 2, panel_y + 100)
            )
            screen.blit(timer_text, timer_rect)

            # Draw Deviation Count below the timer
            deviation_text = self.font.render(
                f"Deviations: {self.deviation_count}", True, WHITE
            )
            deviation_rect = deviation_text.get_rect(
                center=(panel_x + panel_width // 2, panel_y + 130)
            )
            screen.blit(deviation_text, deviation_rect)

        # Call update method in the main loop
        self.update()
