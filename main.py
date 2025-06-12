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
shop_width = 150
shop_height = 50
shop_x = WIDTH // 2 - shop_width // 2
shop_y = HEIGHT - 70
SHOP_COLOR = (0, 180, 100)
shop_button = Button(
    x=shop_x,
    y=shop_y,
    w=shop_width,
    h=shop_height,
    text="Shop",
    font=pygame.font.SysFont(None, 30),
    base_color=(0, 180, 100),
    hover_color=(0, 220, 120)
)

# Settings button
settings_width = 150
settings_height = 50
settings_x = WIDTH - settings_width - 20
settings_y = HEIGHT - 70
SETTINGS_COLOR = (180, 180, 0)
settings_button = Button(
    x=settings_x,
    y=settings_y,
    w=settings_width,
    h=settings_height,
    text="Settings",
    font=pygame.font.SysFont(None, 30),
    base_color=(180, 180, 0),
    hover_color=(220, 220, 0)
)

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

# Shop button
shop_button = Button(
    x=shop_x,
    y=shop_y,
    w=shop_width,
    h=shop_height,
    text="Shop",
    font=pygame.font.SysFont(None, 30),
    base_color=(0, 180, 100),
    hover_color=(0, 220, 120)
)

# Repair logic
repairing = False
repair_progress = 0
REPAIR_SPEED = 1
current_repair_speed = REPAIR_SPEED

# Money
money = 0
money_font = pygame.font.SysFont(None, 36)

# Stats inside
total_repairs = 0
total_money_earned = 0

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
                    total_money_earned += 10

            # Shop button
            elif shop_button.is_clicked(mouse_pos):
                print("Shop clicked")

            # Settings button
            elif settings_button.is_clicked(mouse_pos):
                print("Settings clicked")

            # Stats button
            elif stats_button.is_clicked(mouse_pos):
                show_stats_screen(total_repairs, total_money_earned, current_repair_speed)

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
    shop_button.draw(WINDOW, mouse_pos)

    # Draw settings button
    settings_button.draw(WINDOW, mouse_pos)

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

    # === Show Stats Screen ===
    def show_stats_screen(total_repairs, total_money_earned, current_repair_speed):
        stats_running = True
        while stats_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    stats_running = False

            WINDOW.fill((30, 30, 30))

            title = font.render("Stats", True, WHITE)
            stats = font.render(f"Total Repairs: {total_repairs}", True, WHITE)
            money_stat = font.render(f"Total Money Earned: ${total_money_earned}", True, WHITE)
            speed_stat = font.render(f"Repair Speed: {current_repair_speed}", True, WHITE)
            tip = pygame.font.SysFont(None, 24).render("Press ESC to go back", True, (200, 200, 200))

            WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            WINDOW.blit(stats, (WIDTH // 2 - stats.get_width() // 2, 200))
            WINDOW.blit(money_stat, (WIDTH // 2 - money_stat.get_width() // 2, 260))
            WINDOW.blit(speed_stat, (WIDTH // 2 - speed_stat.get_width() // 2, 320))
            WINDOW.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 400))

            pygame.display.flip()

pygame.quit()
sys.exit()
