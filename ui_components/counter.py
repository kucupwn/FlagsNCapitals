import pygame


class Counter:
    def __init__(self, x: int, y: int) -> None:
        self.font = pygame.font.Font(None, 48)
        self.x = x
        self.y = y

    def draw(self, screen: pygame.Surface, current_count: int, max_count: int) -> None:
        text = f"{current_count} / {max_count}"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)
