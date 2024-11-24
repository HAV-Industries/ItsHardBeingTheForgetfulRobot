import pygame
import os
import time

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)

class Tutorial:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.title_font = pygame.font.Font(None, 40)
        self.desc_font = pygame.font.Font(None, 30)
        self.current_index = 0
        self.hint_duration = 10  # seconds
        self.timer_start = time.time()
        
        # Content array with titles, descriptions, and image paths
        self.content = [
            {
                "title": "Play as a forgetfull robot",
                "description": "",
                "image_path": os.path.join(os.path.dirname(__file__), "img", "hint1.png")
            },
            {
                "title": "Enter commands to harvest crops",
                "description": "Use either the buttons on the screen, or press arrow keys / spacebar",
                "image_path": os.path.join(os.path.dirname(__file__), "img", "hint2.png")
            },
            {
                "title": "Get enough crops, but not too many",
                "description": "Pay attention to the food bar, to make sure you are not collecting too much or too little food.",
                "image_path": os.path.join(os.path.dirname(__file__), "img", "hint3.png")
            },
            {
                "title": "Remember that you don't reme",
                "description": "Pay attention to the food bar, to make sure you are not collecting too much or too little food.",
                "image_path": os.path.join(os.path.dirname(__file__), "img", "hint3.png")
            },
            {
                "title": "If you are able to sustain a sufficient amount of crops throughout multiple stages you win",
                "description": "Ancient system logs could reveal the path forward.",
                "image_path": os.path.join(os.path.dirname(__file__), "img", "hint3.png")
            }
        ]
        
        # Load and scale the current image
        self.load_current_image()

    def load_current_image(self):
        try:
            image = pygame.image.load(self.content[self.current_index]["image_path"]).convert_alpha()
            # Scale image to fit a reasonable size while maintaining aspect ratio
            image_height = 200
            aspect_ratio = image.get_width() / image.get_height()
            image_width = int(image_height * aspect_ratio)
            self.current_image = pygame.transform.scale(image, (image_width, image_height))
        except (pygame.error, FileNotFoundError):
            # Create a placeholder if image loading fails
            self.current_image = pygame.Surface((200, 200))
            self.current_image.fill(GRAY)
            
    def next_hint(self):
        if self.current_index < len(self.content) - 1:
            self.current_index += 1
            self.load_current_image()
            self.timer_start = time.time()  # Reset timer
            return True
        return False

    def draw(self, screen):
        # Fill background
        screen.fill(BLACK)
        
        # Draw current title
        title = self.content[self.current_index]["title"]
        title_surface = self.title_font.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Draw current description
        description = self.content[self.current_index]["description"]
        # Word wrap the description
        words = description.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.desc_font.size(test_line)[0] > self.window_width - 100:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        # Draw each line of the description
        y_offset = 150
        for line in lines:
            desc_surface = self.desc_font.render(line, True, LIGHT_GRAY)
            desc_rect = desc_surface.get_rect(center=(self.window_width // 2, y_offset))
            screen.blit(desc_surface, desc_rect)
            y_offset += 30
        
        # Draw current image
        image_rect = self.current_image.get_rect(center=(self.window_width // 2, y_offset + 120))
        screen.blit(self.current_image, image_rect)
        
        # Draw timer bar
        elapsed_time = time.time() - self.timer_start
        remaining_time = max(0, self.hint_duration - elapsed_time)
        timer_width = 400
        timer_height = 20
        timer_x = (self.window_width - timer_width) // 2
        timer_y = self.window_height - 150
        
        # Draw timer background
        pygame.draw.rect(screen, DARK_GRAY, 
                        (timer_x, timer_y, timer_width, timer_height))
        
        # Draw timer progress
        progress_width = int((remaining_time / self.hint_duration) * timer_width)
        if progress_width > 0:
            pygame.draw.rect(screen, GREEN, 
                           (timer_x, timer_y, progress_width, timer_height))
        
        # Draw timer text
        timer_text = f"{int(remaining_time)}s"
        timer_surface = self.desc_font.render(timer_text, True, WHITE)
        timer_text_rect = timer_surface.get_rect(center=(self.window_width // 2, timer_y - 20))
        screen.blit(timer_surface, timer_text_rect)
        
        # Draw next hint button
        if self.current_index < len(self.content) - 1:
            button_width = 200
            button_height = 40
            button_x = (self.window_width - button_width) // 2
            button_y = self.window_height - 80
            
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            button_hover = button_rect.collidepoint(mouse_pos)
            
            pygame.draw.rect(screen, GRAY if button_hover else LIGHT_GRAY, button_rect, border_radius=5)
            button_text = "Next Hint"
            text_surface = self.desc_font.render(button_text, True, BLACK)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)
            
            # Handle button click
            if button_hover and pygame.mouse.get_pressed()[0]:
                self.next_hint()
        
        # Check if timer has expired
        if remaining_time <= 0:
            self.next_hint()

        # Return True if we're on the last hint and the timer has expired
        return self.current_index == len(self.content) - 1 and remaining_time <= 0
    # Create an instance of the Tutorial class