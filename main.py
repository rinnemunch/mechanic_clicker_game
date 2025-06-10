import pygame
import sys

# Initialize pygame
pygame.init()

# Window
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mechanic Clicker")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
CAR_COLOR = (200, 0, 0)

# Car placeholder
car_x, car_y = 300, 200
car_width, car_height = 200, 100

# Repair button
button_x, button_y = 325, 350
button_width, button_height = 150, 50
BUTTON_COLOR = (0, 120, 215)
button_font = pygame.font.SysFont(None, 30)
button_text = button_font.render("Repair", True, WHITE)
button_text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))

# Repair logic
repairing = False
repair_progress = 0
REPAIR_SPEED = 1

# Money
money = 0

# Font setup
font = pygame.font.SysFont(None, 36)
text_surface = font.render("Car", True, WHITE)
text_rect = text_surface.get_rect(center=(car_x + car_width // 2, car_y + car_height // 2))

# === Main loop ===
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # in FPS
    # === Event Loop ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Repair button clickable
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (button_x <= mouse_x <= button_x + button_width) and (
                    button_y <= mouse_y <= button_y + button_height):
                repairing = True

        # Progress update
        if repairing and repair_progress < 100:
            repair_progress += REPAIR_SPEED
        elif repair_progress >= 100:
            repairing = False

    # Fill background
    WINDOW.fill(GRAY)

    # Draw car placeholder (rectangle)
    pygame.draw.rect(WINDOW, CAR_COLOR, (car_x, car_y, car_width, car_height))
    WINDOW.blit(text_surface, text_rect)

    # Draw repair button
    pygame.draw.rect(WINDOW, BUTTON_COLOR, (button_x, button_y, button_width, button_height))
    WINDOW.blit(button_text, button_text_rect)

    # Progress bar background
    pygame.draw.rect(WINDOW, (100, 100, 100), (button_x, button_y + 60, button_width, 20))

    # Progress bar fill
    fill_width = (repair_progress / 100) * button_width
    pygame.draw.rect(WINDOW, (0, 255, 0), (button_x, button_y + 60, fill_width, 20))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
