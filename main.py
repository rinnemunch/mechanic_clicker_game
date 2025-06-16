import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Background music
background_tracks = [
    "assets/music/track1.mp3",
    "assets/music/track2.mp3",
    "assets/music/track3.mp3",
    "assets/music/track4.mp3",
    "assets/music/track5.mp3"
]

# Money animation (Be aware that I switched from confetti to money pngs)
confetti_frames = []
confetti_path = "assets/money/money_trimmed"

for filename in sorted(os.listdir(confetti_path)):
    if filename.endswith(".png"):
        img = pygame.image.load(os.path.join(confetti_path, filename)).convert_alpha()
        img = pygame.transform.scale(img, (500, 200))
        confetti_frames.append(img)

# Confetti animation state
show_confetti = False
confetti_index = 0
confetti_timer = 0

# Button Colors
BUTTON_BASE = (0, 123, 255)
BUTTON_HOVER = (51, 156, 255)

mechanic_frames = [pygame.image.load("assets/garage_upgrades/mechanic_1.png").convert_alpha(),
                   pygame.image.load("assets/garage_upgrades/mechanic_2.png").convert_alpha()]

mechanic_frames = [pygame.transform.scale(img, (130, 130)) for img in mechanic_frames]

mechanic_frame_index = 0
mechanic_timer = 0
mechanic_interval = 2000

mechanic2_frames = [pygame.image.load("assets/garage_upgrades/mechanic2_1.png").convert_alpha(),
                    pygame.image.load("assets/garage_upgrades/mechanic2_2.png").convert_alpha()]

mechanic2_frames = [pygame.transform.scale(img, (150, 150)) for img in mechanic2_frames]

mechanic2_frame_index = 0
mechanic2_timer = 0
mechanic2_interval = 1200


# Sound effects
repair_sounds = [
    pygame.mixer.Sound("assets/ratchet1.wav"),
    pygame.mixer.Sound("assets/ratchet2.wav"),
    pygame.mixer.Sound("assets/ratchet3.wav")
]
repair_complete_sound = pygame.mixer.Sound("assets/repair_complete.wav")
ui_click_sound = pygame.mixer.Sound("assets/ui_click.wav")
shop_upgrade_sound = pygame.mixer.Sound("assets/shop_upgrade.wav")
sound_enabled = True
music_enabled = True
repair_channel = pygame.mixer.Channel(1)


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


def handle_upgrade():
    global money, repair_upgrade_level, REPAIR_SPEED, upgrade_cost, current_repair_speed
    if repair_upgrade_level < max_repair_level and money >= upgrade_cost:
        money -= upgrade_cost
        repair_upgrade_level += 1
        REPAIR_SPEED = repair_upgrade_level
        current_repair_speed = REPAIR_SPEED
        upgrade_cost += 25
        print(f"Upgraded to level {repair_upgrade_level}. New speed: {REPAIR_SPEED}")
        if sound_enabled:
            shop_upgrade_sound.play()
    else:
        print("Not enough money or already maxed")


def handle_passive_upgrade():
    global money, passive_income_level, passive_income_amount, passive_upgrade_cost
    if passive_income_level < max_passive_level and money >= passive_upgrade_cost:
        money -= passive_upgrade_cost
        passive_income_level += 1
        passive_income_amount += 1  # amount earned in seconds
        passive_upgrade_cost += 75
        if sound_enabled:
            shop_upgrade_sound.play()
        print(f"Passive Income Level: {passive_income_level}")
    else:
        print("Not enough money or max level reached.")


# Looping through background tracks
last_track = None


def play_random_track():
    global last_track
    if not music_enabled:
        return

    new_track = random.choice(background_tracks)
    while new_track == last_track and len(background_tracks) > 1:
        new_track = random.choice(background_tracks)
    last_track = new_track
    print(f"Now playing: {new_track}")
    pygame.mixer.music.load(new_track)
    pygame.mixer.music.play()

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
        tip = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 24).render("Press ESC to go back", True,
                                                                                      (200, 200, 200))

        WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        WINDOW.blit(stats, (WIDTH // 2 - stats.get_width() // 2, 200))
        WINDOW.blit(money_stat, (WIDTH // 2 - money_stat.get_width() // 2, 260))
        WINDOW.blit(speed_stat, (WIDTH // 2 - speed_stat.get_width() // 2, 320))
        WINDOW.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 400))

        pygame.display.flip()


def show_shop_screen():
    global upgrade_button_rect

    shop_running = True
    while shop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                shop_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if upgrade_button_rect.collidepoint(mouse):
                    handle_upgrade()
                if passive_button_rect.collidepoint(mouse):
                    handle_passive_upgrade()

        # Background
        WINDOW.fill((20, 20, 20))

        # Title
        title = font.render("Shop", True, WHITE)
        WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Upgrade button
        upgrade_text = f"Upgrade Repair Speed (Lvl {repair_upgrade_level}/{max_repair_level}) - ${upgrade_cost}"
        upgrade_surface = font.render(upgrade_text, True, WHITE)
        upgrade_button_rect = upgrade_surface.get_rect(center=(WIDTH // 2, 200))
        pygame.draw.rect(WINDOW, (0, 100, 255), upgrade_button_rect.inflate(20, 10), border_radius=10)
        WINDOW.blit(upgrade_surface, upgrade_button_rect)

        # Passive income upgrade button
        passive_text = f"Increase Passive Income (Lvl {passive_income_level}/{max_passive_level}) - ${passive_upgrade_cost}"
        passive_surface = font.render(passive_text, True, WHITE)
        passive_button_rect = passive_surface.get_rect(center=(WIDTH // 2, 300))
        pygame.draw.rect(WINDOW, (255, 140, 0), passive_button_rect.inflate(20, 10), border_radius=10)
        WINDOW.blit(passive_surface, passive_button_rect)

        # Tip
        tip = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 24).render("Press ESC to return", True,
                                                                                      (200, 200, 200))
        WINDOW.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 400))

        pygame.display.flip()


# Garage Visual Upgrades
flag_img = pygame.image.load("assets/garage_upgrades/flag.png").convert_alpha()
flag_img = pygame.transform.scale(flag_img, (100, 100))
board_img = pygame.image.load("assets/garage_upgrades/bulletin_board.png").convert_alpha()
board_img = pygame.transform.scale(board_img, (100, 100))
clock_img = pygame.image.load("assets/garage_upgrades/clock.png").convert_alpha()
clock_img = pygame.transform.scale(clock_img, (100, 100))
poster_img = pygame.image.load("assets/garage_upgrades/poster.png").convert_alpha()
poster_img = pygame.transform.scale(poster_img, (100, 100))
neon_img = pygame.image.load("assets/garage_upgrades/neon_sign.png").convert_alpha()
neon_img = pygame.transform.scale(neon_img, (100, 100))
tires_img = pygame.image.load("assets/garage_upgrades/tires.png").convert_alpha()
tires_img = pygame.transform.scale(tires_img, (100, 100))
trophy_img = pygame.image.load("assets/garage_upgrades/trophy.png").convert_alpha()
trophy_img = pygame.transform.scale(trophy_img, (100, 100))
pygame.display.set_caption("Mechanic Clicker")
play_random_track()

main_background = pygame.image.load("assets/main_bg.png").convert()
main_background = pygame.transform.scale(main_background, (WIDTH, HEIGHT))

# Loading Car Sprites
car_sprites = []


def load_car(filename, size, y_offset=0):
    img = pygame.image.load(os.path.join("assets/cars", filename)).convert_alpha()
    img = pygame.transform.scale(img, size)
    return img, y_offset


car_sprites.append(load_car("beetle_red.png", (340, 240), 20))
car_sprites.append(load_car("boxtruck.png", (340, 240), -10))
car_sprites.append(load_car("cybertruck.png", (450, 260), 10))
car_sprites.append(load_car("green_sportscar.png", (340, 240), 28))
car_sprites.append(load_car("mclaren_8bit.png", (340, 240), 0))
car_sprites.append(load_car("miata.png", (340, 240), 20))
car_sprites.append(load_car("corvette_c5.png", (340, 240), 20))
car_sprites.append(load_car("purple_countach.png", (360, 240), 12))
car_sprites.append(load_car("black_firebird.png", (340, 240), 15))
car_sprites.append(load_car("blue_mustang.png", (340, 240), 20))

current_car, car_offset = random.choice(car_sprites)
last_car = None

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
CAR_COLOR = (200, 0, 0)

# Car
car_x, car_y = 250, 150
car_width, car_height = 200, 100

# Repair button
button_x, button_y = 325, 350
button_width, button_height = 150, 50
BUTTON_COLOR = (0, 120, 215)
button_font = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30)
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
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
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
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)

# Stats button
stats_font = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30)
stats_button = Button(
    x=20,
    y=HEIGHT - 70,
    w=150,
    h=50,
    text="Stats",
    font=stats_font,
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)

# Sounds Toggle Button
sound_toggle_button = Button(
    x=WIDTH // 2 - 100,
    y=250,
    w=200,
    h=50,
    text="Sound: On",
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)

# Music Toggle Button
music_toggle_button = Button(
    x=WIDTH // 2 - 100,
    y=320,
    w=200,
    h=50,
    text="Music: On",
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)
# Skip track
skip_track_button = Button(
    x=WIDTH // 2 - 100,
    y=390,
    w=200,
    h=50,
    text="Skip Track",
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)


# Repair Button
repair_button = Button(
    x=button_x,
    y=button_y,
    w=button_width,
    h=button_height,
    text="Repair",
    font=pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 30),
    base_color=BUTTON_BASE,
    hover_color=BUTTON_HOVER
)

# Repair logic
repairing = False
repair_progress = 0
repair_upgrade_level = 1
max_repair_level = 10
upgrade_cost = 25
REPAIR_SPEED = repair_upgrade_level
current_repair_speed = REPAIR_SPEED
current_car, car_offset = random.choice(car_sprites)

# Passive income
passive_income_level = 0
max_passive_level = 10
passive_income_amount = 0
passive_upgrade_cost = 100
last_passive_tick = pygame.time.get_ticks()

# Money
money = 0
money_font = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 48)

# Stats inside
total_repairs = 0
total_money_earned = 0

# Font setup
font = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 36)
text_surface = font.render("Car", True, WHITE)
text_rect = text_surface.get_rect(center=(car_x + car_width // 2, car_y + car_height // 2))


def show_settings_screen():
    global sound_enabled
    global music_enabled

    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                settings_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_toggle_button.is_clicked(pygame.mouse.get_pos()):
                    sound_enabled = not sound_enabled
                    if sound_enabled:
                        sound_toggle_button.text = "Sound: On"
                        if sound_enabled:
                            ui_click_sound.play()
                    else:
                        sound_toggle_button.text = "Sound: Off"

                    sound_toggle_button.text_surf = sound_toggle_button.font.render(
                        sound_toggle_button.text, True, (255, 255, 255)
                    )
                    sound_toggle_button.text_rect = sound_toggle_button.text_surf.get_rect(
                        center=sound_toggle_button.rect.center
                    )

                if music_toggle_button.is_clicked(pygame.mouse.get_pos()):
                    music_enabled = not music_enabled
                    if music_enabled:
                        music_toggle_button.text = "Music: On"
                        if sound_enabled:
                            ui_click_sound.play()
                        if not pygame.mixer.music.get_busy():
                            play_random_track()
                    else:
                        music_toggle_button.text = "Music: Off"
                        pygame.mixer.music.stop()

                    music_toggle_button.text_surf = music_toggle_button.font.render(
                        music_toggle_button.text, True, (255, 255, 255)
                    )
                    music_toggle_button.text_rect = music_toggle_button.text_surf.get_rect(
                        center=music_toggle_button.rect.center
                    )

                if skip_track_button.is_clicked(pygame.mouse.get_pos()):
                    if sound_enabled:
                        ui_click_sound.play()
                    play_random_track()

        # Background and text
        WINDOW.fill((25, 25, 25))
        title = font.render("Settings", True, WHITE)
        tip = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 24).render("Press ESC to return", True,
                                                                                      (200, 200, 200))
        WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        WINDOW.blit(tip, (WIDTH // 2 - tip.get_width() // 2, 460))

        # Draw sound toggle
        sound_toggle_button.draw(WINDOW, pygame.mouse.get_pos())
        music_toggle_button.draw(WINDOW, pygame.mouse.get_pos())
        skip_track_button.draw(WINDOW, pygame.mouse.get_pos())

        pygame.display.flip()


# === Main loop ===
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    now = pygame.time.get_ticks()
    if not pygame.mixer.music.get_busy():
        play_random_track()
    if now - last_passive_tick >= 1000:
        money += passive_income_amount
        total_money_earned += passive_income_amount
        last_passive_tick = now

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Repair button
            if repair_button.is_clicked(mouse_pos):
                if repair_progress < 100:
                    repair_progress += 10
                    if sound_enabled:
                        random.choice(repair_sounds).play()
                else:
                    repair_progress = 0
                    money += 10
                    total_repairs += 1
                    total_money_earned += 10
                    while True:
                        new_car, new_offset = random.choice(car_sprites)
                        if new_car != current_car:
                            break
                    current_car, car_offset = new_car, new_offset
                    last_car = current_car
                    show_confetti = True
                    confetti_index = 0
                    confetti_timer = pygame.time.get_ticks()
                    if sound_enabled:
                        repair_channel.play(repair_complete_sound)


            # Shop button
            elif shop_button.is_clicked(mouse_pos):
                if sound_enabled:
                    ui_click_sound.play()
                show_shop_screen()

            # Settings button
            elif settings_button.is_clicked(mouse_pos):
                if sound_enabled:
                    ui_click_sound.play()
                show_settings_screen()

            # Stats button
            elif stats_button.is_clicked(mouse_pos):
                ui_click_sound.play()
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
    WINDOW.blit(main_background, (0, 0))

    # Draw car
    if current_car == car_sprites[2][0]:  # Cybertruck
        WINDOW.blit(current_car, (car_x - 30, car_y + car_offset))
    else:
        WINDOW.blit(current_car, (car_x, car_y + car_offset))

    # Draw confetti
    if show_confetti:
        current_time = pygame.time.get_ticks()
        if confetti_index < len(confetti_frames):
            if current_time - confetti_timer > 30:
                confetti_timer = current_time
                confetti_index += 1
            if confetti_index < len(confetti_frames):
                WINDOW.blit(confetti_frames[confetti_index], (car_x - 60, car_y - 10))  # Adjustable
        else:
            show_confetti = False

    # Passive income visuals
    if passive_income_level >= 1:
        WINDOW.blit(flag_img, (50, 60))
    if passive_income_level >= 2:
        WINDOW.blit(board_img, (180, 60))
    if passive_income_level >= 3:
        WINDOW.blit(clock_img, (310, 60))
    if passive_income_level >= 4:
        WINDOW.blit(poster_img, (440, 60))
    if passive_income_level >= 5:
        WINDOW.blit(neon_img, (570, 60))
    if passive_income_level >= 6:
        WINDOW.blit(tires_img, (180, 480))
    if passive_income_level >= 7:
        WINDOW.blit(trophy_img, (660, 275))
    if passive_income_level >= 8:
        now = pygame.time.get_ticks()
        if now - mechanic_timer > mechanic_interval:
            mechanic_frame_index = (mechanic_frame_index + 1) % len(mechanic_frames)
            mechanic_timer = now
        WINDOW.blit(mechanic_frames[mechanic_frame_index], (440, 480))
    if passive_income_level >= 9:
        now = pygame.time.get_ticks()
        if now - mechanic2_timer > mechanic2_interval:
            mechanic2_frame_index = (mechanic2_frame_index + 1) % len(mechanic2_frames)
            mechanic2_timer = now
        WINDOW.blit(mechanic2_frames[mechanic2_frame_index], (520, 490))

    # Draw repair button
    repair_button.draw(WINDOW, mouse_pos)

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
    color = (0, 255, 0) if money > 0 else (255, 0, 0)
    money_text = money_font.render(f"${money}", True, color)
    money_rect = money_text.get_rect(center=(WIDTH // 2, 30))
    WINDOW.blit(money_text, money_rect)

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
