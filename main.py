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

# Font setup
font = pygame.font.SysFont(None, 36)
text_surface = font.render("Car", True, WHITE)
text_rect = text_surface.get_rect(center=(car_x + car_width // 2, car_y + car_height // 2))

# === Main loop ===
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # in FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    WINDOW.fill(GRAY)

    # Draw car placeholder (rectangle)
    pygame.draw.rect(WINDOW, CAR_COLOR, (car_x, car_y, car_width, car_height))
    WINDOW.blit(text_surface, text_rect)

    # Draw repair button
    pygame.draw.rect(WINDOW, BUTTON_COLOR, (button_x, button_y, button_width, button_height))
    WINDOW.blit(button_text, button_text_rect)

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
