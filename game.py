import pygame
import os
import random
from rapidfuzz import fuzz
from ui_components.input_box import InputBox
from ui_components.button import Button
from ui_components.answer_label import AnswerLabel
from ui_components.counter import Counter
from ui_components.capitals import Capitals
from utils.img_loader import get_resource_path


class Flags:
    def __init__(self) -> None:
        self.width = 1280
        self.height = 720
        self.background_color = (255, 240, 210)
        self.flags_dir = "flags"
        self.flag_list = self.get_flag_list()
        self.checked_flags = []
        self.current_flag_name = ""
        self.current_flag_img = None
        self.image_container = pygame.Rect(
            self.width // 2 - 200, self.height // 2 - 250, 400, 300
        )
        self.answer_label_y_pos = self.image_container.bottom + 40
        self.running = True
        self.finished = False
        self.shown = False

        self.init_pygame()
        self.input_box = InputBox(self.width, self.height)
        self.show_button = Button("Show", 40, 50, 120, 40)
        self.next_button = Button("Next", self.width - 160, 50, 120, 40)
        self.answer_label = AnswerLabel()
        self.counter = Counter(self.width - 100, self.height - 50)
        self.capitals = Capitals(self.width, self.height)
        self.win_img = pygame.image.load(get_resource_path("utils/Congrat.PNG"))
        self.load_random_flag()

    def init_pygame(self) -> None:
        """
        Initiatiates pygame with clock and window caption
        """

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags")

    def get_flag_list(self) -> list:
        """
        Returns flag list as list (containing extension)
        """

        flags_path = get_resource_path(self.flags_dir)
        return [flag for flag in os.listdir(flags_path)]

    def is_finished(self) -> bool:
        """
        Checks if all flags are guessed correctly
        """

        if len(self.checked_flags) == len(self.flag_list):
            self.current_flag_img = None
            self.finished = True
            return True
        else:
            return False

    def scale_image(self, image: pygame.Surface) -> pygame.Surface:
        """
        Scales image to fit container for homogenous size
        """

        img_width, img_height = image.get_size()
        container_width, container_height = self.image_container.size

        scale_width = container_width / img_width
        scale_height = container_height / img_height

        scale = min(scale_width, scale_height)
        new_size = (int(img_width * scale), int(img_height * scale))

        return pygame.transform.smoothscale(image, new_size)

    def load_random_flag(self) -> None:
        """
        Loads a scaled random flag
        Sets as current answer
        """

        while True:
            filename = random.choice(self.flag_list)
            self.current_flag_name = os.path.splitext(filename)[0]

            if self.current_flag_name in self.checked_flags:
                continue
            else:
                break

        img_path = get_resource_path(os.path.join(self.flags_dir, filename))
        image = pygame.image.load(img_path).convert_alpha()
        self.current_flag_img = self.scale_image(image)

        self.answer_label.set_answer(self.current_flag_name)
        self.current_flag_name_lower = [
            word.lower() for word in self.current_flag_name.split()
        ]

        self.capitals.set_current_answer(self.current_flag_name)

    def check_answer(self, answer: str) -> None:
        """
        Checks user input
        Using fuzzywuzzy for handling typos
        Checks, if any word (excluding some, like 'the') matches
        On correct input, reveals answer, also adds to checked flags
        """

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

    def event_handler(self) -> None:
        """
        Handles exit, input, buttons
        """

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

    def display_win(self) -> None:
        """
        Displays win image and label
        """

        self.answer_label.set_answer("All flags are completed")
        self.answer_label.reveal()
        self.display_image(self.win_img)

    def display_image(self, image: pygame.Surface) -> None:
        """
        Displays image in container
        Special rule for answer label on win
        """

        rect = image.get_rect(center=self.image_container.center)
        self.screen.blit(image, rect)

        if self.finished:
            self.answer_label_y_pos = rect.top - 60

    def update(self) -> None:
        """
        Update function for displaying everything
        Displays ui elements until finished
        """

        self.clock.tick(60)
        self.screen.fill(self.background_color)

        if self.finished:
            self.display_win()
        else:
            self.input_box.add_search_label(self.screen)
            self.input_box.draw(self.screen)
            self.show_button.draw(self.screen)
            self.next_button.draw(self.screen)
            self.counter.draw(self.screen, len(self.checked_flags), len(self.flag_list))

        if self.current_flag_img:
            self.display_image(self.current_flag_img)

        self.answer_label.draw(self.screen, self.width // 2, self.answer_label_y_pos)

        self.capitals.draw(self.screen)

        pygame.display.flip()

    def main_loop(self) -> None:
        """
        Main logic wrapped here
        """

        while self.running:
            self.event_handler()
            self.update()


game = Flags()
game.main_loop()
