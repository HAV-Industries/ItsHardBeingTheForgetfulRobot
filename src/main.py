import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 8
MIN_CELL_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1
current_screen = TITLE_SCREEN


def get_cell_size():
    width_based = (WINDOW_WIDTH - 100) // GRID_SIZE
    height_based = (WINDOW_HEIGHT - 100) // GRID_SIZE
    return max(min(width_based, height_based), MIN_CELL_SIZE)


def draw_title_screen(screen, font):
    global current_screen

    # Draw title
    title = "The Robot has Taken Over!"
    title_surface = font.render(title, True, DARK_GRAY)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 200))
    screen.blit(title_surface, title_rect)

    # Draw button
    button_width = 200
    button_height = 50
    button_x = (WINDOW_WIDTH - button_width) // 2
    button_y = 350
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Check mouse hover
    mouse_pos = pygame.mouse.get_pos()
    button_hover = button_rect.collidepoint(mouse_pos)

    # Draw button with hover effect
    pygame.draw.rect(
        screen, GRAY if button_hover else LIGHT_GRAY, button_rect, border_radius=10
    )

    # Draw button text
    button_text = "Start Game"
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Handle click
    if button_hover and pygame.mouse.get_pressed()[0]:
        current_screen = GAME_SCREEN


def draw_game_screen(screen):
    cell_size = get_cell_size()
    grid_pixel_size = GRID_SIZE * cell_size

    # Center the grid
    start_x = (WINDOW_WIDTH - grid_pixel_size) // 2
    start_y = (WINDOW_HEIGHT - grid_pixel_size) // 2

    # Draw grid
    for i in range(GRID_SIZE + 1):
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


def main():
    global current_screen

    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("The Robot has Taken Over!")

    # Set up font
    font = pygame.font.Font(None, 40)  # None uses default system font

    clock = pygame.time.Clock()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen
        screen.fill(WHITE)

        # Draw current screen
        if current_screen == TITLE_SCREEN:
            draw_title_screen(screen, font)
        elif current_screen == GAME_SCREEN:
            draw_game_screen(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
