import pygame
import sys

# Initialize pygame
pygame.init()


class Button:
    def __init__(self, x, y, w, h, text, font, base_color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color

        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.base_color

        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=25)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


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

# Shop button
shop_x = button_x + button_width + 20
shop_y = button_y
shop_width = 150
shop_height = 50
SHOP_COLOR = (0, 180, 100)
shop_font = pygame.font.SysFont(None, 30)
shop_text = shop_font.render("Shop", True, WHITE)
shop_text_rect = shop_text.get_rect(center=(shop_x + shop_width // 2, shop_y + shop_height // 2))

# Settings button
settings_x = shop_x + shop_width + 20
settings_y = button_y
settings_width = 150
settings_height = 50
SETTINGS_COLOR = (180, 180, 0)
settings_font = pygame.font.SysFont(None, 30)
settings_text = settings_font.render("Settings", True, WHITE)
settings_text_rect = settings_text.get_rect(
    center=(settings_x + settings_width // 2, settings_y + settings_height // 2))

# Stats button
stats_font = pygame.font.SysFont(None, 30)
stats_button = Button(
    x=20,
    y=HEIGHT - 70,
    w=150,
    h=50,
    text="Stats",
    font=stats_font,
    base_color=(128, 0, 128),
    hover_color=(170, 0, 170)
)


# Repair logic
repairing = False
repair_progress = 0
REPAIR_SPEED = 1

# Money
money = 0
money_font = pygame.font.SysFont(None, 36)

# Stats inside
total_repairs = 0

# Font setup
font = pygame.font.SysFont(None, 36)
text_surface = font.render("Car", True, WHITE)
text_rect = text_surface.get_rect(center=(car_x + car_width // 2, car_y + car_height // 2))

# === Main loop ===
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    # === Event Loop ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # === MOUSEDOWN LOGIC ===

        # DEV TEST CTRL SHIFT M
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if (event.key == pygame.K_m and
                    mods & pygame.KMOD_CTRL and
                    mods & pygame.KMOD_SHIFT):
                money += 100

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Repair button
            if (button_x <= mouse_x <= button_x + button_width) and (
                    button_y <= mouse_y <= button_y + button_height):
                if repair_progress < 100:
                    repair_progress += 10
                else:
                    repair_progress = 0
                    money += 10
                    total_repairs += 1

            # Shop button
            elif (shop_x <= mouse_x <= shop_x + shop_width) and (
                    shop_y <= mouse_y <= shop_y + shop_height):
                print("Shop clicked")

            # Settings button
            elif (settings_x <= mouse_x <= settings_x + settings_width) and (
                    settings_y <= mouse_y <= settings_y + settings_height):
                print("Settings clicked")

            # Stats button
            elif stats_button.is_clicked(mouse_pos):
                print("Stats clicked")

        # Progress update
        if repairing:
            if repair_progress < 100:
                repair_progress += REPAIR_SPEED
            else:
                repairing = False
                repair_progress = 0
                money += 10

    # Fill background
    WINDOW.fill(GRAY)

    # Draw car placeholder (rectangle)
    pygame.draw.rect(WINDOW, CAR_COLOR, (car_x, car_y, car_width, car_height))
    WINDOW.blit(text_surface, text_rect)

    # Draw repair button
    pygame.draw.rect(WINDOW, BUTTON_COLOR, (button_x, button_y, button_width, button_height))
    WINDOW.blit(button_text, button_text_rect)

    # Draw shop button
    pygame.draw.rect(WINDOW, SHOP_COLOR, (shop_x, shop_y, shop_width, shop_height))
    WINDOW.blit(shop_text, shop_text_rect)

    # Draw settings button
    pygame.draw.rect(WINDOW, SETTINGS_COLOR, (settings_x, settings_y, settings_width, settings_height))
    WINDOW.blit(settings_text, settings_text_rect)

    # Draw stats button
    stats_button.draw(WINDOW, mouse_pos)

    # Progress bar background
    pygame.draw.rect(WINDOW, (100, 100, 100), (button_x, button_y + 60, button_width, 20))

    # Progress bar fill
    fill_width = (repair_progress / 100) * button_width
    pygame.draw.rect(WINDOW, (0, 255, 0), (button_x, button_y + 60, fill_width, 20))

    # Draw money text
    money_text = money_font.render(f"${money}", True, WHITE)
    WINDOW.blit(money_text, (20, 20))

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
