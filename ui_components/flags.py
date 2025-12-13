import pygame
import os
import random
from utils.asset_loader import get_resource_path
from rapidfuzz import fuzz
from ui_components.answer_label import CountryAnswerLabel


class Flags:
    def __init__(self, screen_width: int, screen_height: int):
        self.flags_dir = "flags"
        self.flag_list = self.get_flag_list()
        self.current_flag_name = ""
        self.current_flag_img = None
        self.answer_label = CountryAnswerLabel()
        self.image_container = pygame.Rect(
            screen_width // 2 - 200, screen_height // 2 - 250, 400, 300
        )
        self.answer_label_y_pos = self.image_container.bottom + 40
        self.shown = False

    def get_flag_list(self) -> list:
        """
        Returns flag list as list (containing extension)
        """

        flags_path = get_resource_path(self.flags_dir)
        return [flag for flag in os.listdir(flags_path)]

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

    def load_random_flag(self, checked_countries: list) -> None:
        """
        Loads a scaled random flag
        Sets as current answer
        """

        while True:
            filename = random.choice(self.flag_list)
            self.current_flag_name = os.path.splitext(filename)[0]

            if self.current_flag_name in checked_countries:
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

    def check_answer(self, answer: str) -> bool:
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
            return True
