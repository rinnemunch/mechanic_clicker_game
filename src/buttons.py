import pygame


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
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=25)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class FloatingText:
    def __init__(self, text, x, y, duration=1000):
        self.text = text
        self.x = x
        self.y = y
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.alpha = 255
        self.font = pygame.font.Font("assets/Roboto-VariableFont_wdth,wght.ttf", 28)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        self.y -= 0.3
        self.alpha = max(255 - (elapsed / self.duration) * 255, 0)
        return elapsed < self.duration

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, (0, 255, 0))
        text_surf.set_alpha(int(self.alpha))
        surface.blit(text_surf, (self.x, self.y))
