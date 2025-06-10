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

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
