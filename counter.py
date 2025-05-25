import pygame


class Counter:
    def __init__(self, x, y):
        self.font = pygame.font.Font(None, 64)
        self.x = x
        self.y = y

    def draw(self, screen, current_count, max_count):
        text = f"{current_count} / {max_count}"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
