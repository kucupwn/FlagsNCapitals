import pygame
from button import Button


class Capitals:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.button_width = 120
        self.button_height = 60
        self.spacing = 20
        self.answers = ["a", "b", "c", "d"]
        self.buttons = []
        self.start_x = (screen_width - (self.button_width * 2 + self.spacing)) // 2
        self.start_y = (screen_height - (self.button_height * 2 + self.spacing)) // 2

    def get_buttons(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def event_handler(self):
        pass

    def check_answer(self):
        pass
