import pygame
import os
import random
from fuzzywuzzy import fuzz
from input_box import InputBox
from button import Button
from answer_label import AnswerLabel

BACKGROUND = (255, 255, 255)


class Flags:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.flags_dir = "flags"
        self.flag_list = self.get_flag_list()
        self.current_flag_name = ""
        self.current_flag_img = None
        self.running = True

        self.init_pygame()
        self.input_box = InputBox(self.width, self.height)
        self.give_up_button = Button("Give Up", 40, 50, 120, 40)
        self.next_button = Button("Next", self.width - 160, 50, 120, 40)
        self.answer_label = AnswerLabel()
        self.load_random_flag()

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags")

    def get_flag_list(self):
        return [flag for flag in os.listdir(self.flags_dir)]

    def load_random_flag(self):
        filename = random.choice(self.flag_list)
        self.current_flag_name = os.path.splitext(filename)[0]
        img_path = os.path.join(self.flags_dir, filename)
        self.current_flag_img = pygame.image.load(img_path)
        self.answer_label.set_answer(self.current_flag_name)
        self.current_flag_name_lower = [
            word.lower() for word in self.current_flag_name.split()
        ]

    def check_answer(self, answer: str):
        exclude_words = ["and", "of", "the"]
        threshold = 80
        matches = 0

        correct_parts = [
            word for word in self.current_flag_name_lower if word not in exclude_words
        ]
        answer_parts = [
            word.lower() for word in answer.split() if word not in exclude_words
        ]

        for answer_word in answer_parts:
            for correct_word in correct_parts:
                similarity = fuzz.ratio(answer_word, correct_word)
                if similarity >= threshold:
                    matches += 1
                    break

        if matches >= 2 or (len(correct_parts) == 1 and matches == 1):
            self.answer_label.reveal()

    def event_handler(self):
        for event in pygame.event.get():
            # Handle exit
            if event.type == pygame.QUIT:
                self.running = False

            input_text = self.input_box.event_handler(event)
            if input_text:
                self.check_answer(input_text)

            if self.next_button.is_clicked(event) or (
                input_text == ""
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
            ):
                self.load_random_flag()
                self.input_box.set_active()

            if self.give_up_button.is_clicked(event):
                self.answer_label.reveal()
                self.input_box.set_active()

    def update(self):
        self.clock.tick(60)
        self.screen.fill(BACKGROUND)
        self.input_box.add_search_label(self.screen)
        self.input_box.draw(self.screen)
        self.give_up_button.draw(self.screen)
        self.next_button.draw(self.screen)

        if self.current_flag_img:
            rect = self.current_flag_img.get_rect(
                center=(self.width // 2, self.height // 2 - 30)
            )
            self.screen.blit(self.current_flag_img, rect)

            self.answer_label.draw(self.screen, self.width // 2, rect.bottom + 100)

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.event_handler()
            self.update()


game = Flags()
game.main_loop()
