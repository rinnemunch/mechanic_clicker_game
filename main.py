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

# Font setup
font = pygame.font.SysFont(None, 36)
text_surface = font.render("Car", True, WHITE)
text_rect = text_surface.get_rect(center=(car_x + car_width // 2, car_y + car_height // 2))

# Main loop
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

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
