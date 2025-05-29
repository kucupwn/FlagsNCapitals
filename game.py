import pygame
import os
import random
from fuzzywuzzy import fuzz
from ui_components.input_box import InputBox
from ui_components.button import Button
from ui_components.answer_label import AnswerLabel
from ui_components.counter import Counter

BACKGROUND = (255, 240, 210)


class Flags:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.flags_dir = "flags"
        self.flag_list = self.get_flag_list()
        self.checked_flags = []
        self.current_flag_name = ""
        self.current_flag_img = None
        self.image_container = pygame.Rect(
            self.width // 2 - 200, self.height // 2 - 150, 400, 300
        )
        self.running = True
        self.finished = False
        self.shown = False

        self.init_pygame()
        self.input_box = InputBox(self.width, self.height)
        self.show_button = Button("Show", 40, 50, 120, 40)
        self.next_button = Button("Next", self.width - 160, 50, 120, 40)
        self.answer_label = AnswerLabel()
        self.counter = Counter(self.width - 100, self.height - 50)
        self.win_img = pygame.image.load("utils/Congrat.PNG")
        self.load_random_flag()

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags")

    def get_flag_list(self):
        return [flag for flag in os.listdir(self.flags_dir)]

    def is_finished(self) -> bool:
        if len(self.checked_flags) == len(self.flag_list):
            self.current_flag_img = None
            self.finished = True
            return True
        else:
            return False

    def scale_image(self, image: pygame.Surface):
        img_width, img_height = image.get_size()
        container_width, container_height = self.image_container.size

        scale_width = container_width / img_width
        scale_height = container_height / img_height

        scale = min(scale_width, scale_height)
        new_size = (int(img_width * scale), int(img_height * scale))

        return pygame.transform.smoothscale(image, new_size)

    def load_random_flag(self):
        while True:
            filename = random.choice(self.flag_list)
            self.current_flag_name = os.path.splitext(filename)[0]

            if self.current_flag_name in self.checked_flags:
                continue
            else:
                break

        img_path = os.path.join(self.flags_dir, filename)
        image = pygame.image.load(img_path).convert_alpha()
        self.current_flag_img = self.scale_image(image)

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

        if matches >= 1 or (len(correct_parts) == 1 and matches == 1):
            self.answer_label.reveal()
            self.checked_flags.append(self.current_flag_name)

    def event_handler(self):
        for event in pygame.event.get():
            # Handle exit
            if event.type == pygame.QUIT:
                self.running = False

            input_text = self.input_box.event_handler(event)
            if input_text and not self.shown:
                self.check_answer(input_text)

            if self.next_button.is_clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
            ):
                if not self.is_finished():
                    self.load_random_flag()
                    self.input_box.set_active()
                    self.shown = False

            if self.show_button.is_clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_F1
            ):
                self.answer_label.reveal()
                self.input_box.set_active()
                self.shown = True

    def display_win(self):
        self.answer_label.set_answer("All flags are completed")
        self.answer_label.reveal()
        self.display_image(self.win_img)

    def display_image(self, image):
        rect = image.get_rect(center=self.image_container.center)
        self.screen.blit(image, rect)
        self.y_pos = rect.bottom + 60

    def update(self):
        self.clock.tick(60)
        self.screen.fill(BACKGROUND)

        if self.finished:
            self.display_win()

        self.input_box.add_search_label(self.screen)
        self.input_box.draw(self.screen)
        self.show_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.counter.draw(self.screen, len(self.checked_flags), len(self.flag_list))

        if self.current_flag_img:
            self.display_image(self.current_flag_img)

        self.answer_label.draw(self.screen, self.width // 2, self.y_pos)

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.event_handler()
            self.update()


game = Flags()
game.main_loop()
