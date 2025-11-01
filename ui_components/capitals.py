import pygame
import json
from random import sample, shuffle
from .button import Button


class Capitals:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.capitals = self.get_country_capitals()
        self.button_width = 300
        self.button_height = 60
        self.spacing = 20
        self.current_country = ""
        self.current_capital = None
        self.answers = []
        self.buttons = []
        self.start_x = (screen_width - (self.button_width * 2 + self.spacing)) // 2
        self.start_y = (
            screen_height
            - (self.button_height * 2 + self.spacing)
            - (screen_height * 0.1)
        )
        self.shown = False
        self.tried = False
        self.green = (0, 200, 0)
        self.red = (200, 0, 0)

    def get_country_capitals(self) -> dict:
        with open("capitals/country_capitals.json", "r", encoding="utf-8") as f:
            country_capitals = list(json.load(f).items())
            return country_capitals

    def get_buttons(self):
        for i, text in enumerate(self.answers):
            row = i // 2
            col = i % 2
            x = self.start_x + col * (self.button_width + self.spacing)
            y = self.start_y + row * (self.button_height + self.spacing)
            self.buttons.append(
                Button(text, x, y, self.button_width, self.button_height)
            )

    def set_current_answer(self, current_country: str):
        self.current_country = current_country

        self.current_capital = None
        for country, capital in self.capitals:
            if country == current_country:
                self.current_capital = capital
                break

        if self.current_capital is None:
            self.answers = []
            self.buttons = []
            self.shown = False
            return

        self.get_answers()

    def get_answers(self):
        wrong_capitals = [
            capital for _, capital in self.capitals if capital != self.current_capital
        ]

        selected_wrong = sample(wrong_capitals, 3)
        self.answers = selected_wrong + [self.current_capital]
        shuffle(self.answers)

        self.tried = False
        self.buttons = []
        self.get_buttons()

    def draw(self, screen: pygame.Surface):
        for button in self.buttons:
            button.draw(screen)

    def event_handler(self, event):
        if not self.tried:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event):
                        self.tried = True
                        selected = button.text
                        if selected == self.current_capital:
                            button.color = self.green
                            return True
                        else:
                            button.color = self.red
                            return False
            return None
