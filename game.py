import pygame

# from rapidfuzz import fuzz
from ui_components.input_box import InputBox
from ui_components.button import Button
from ui_components.counter import Counter
from ui_components.flags import Flags
from ui_components.capitals import Capitals
from utils.img_loader import get_resource_path


class Game:
    def __init__(self) -> None:
        self.width = 1280
        self.height = 720
        self.background_color = (255, 240, 210)
        self.checked_countries = []
        self.running = True
        self.finished = False

        self.init_pygame()
        self.input_box = InputBox(self.width, self.height)
        self.show_button = Button("Show", 40, 50, 120, 40)
        self.next_button = Button("Next", self.width - 160, 50, 120, 40)
        self.counter = Counter(self.width - 100, self.height - 50)
        self.flags = Flags(self.width, self.height)
        self.capitals = Capitals(self.width, self.height)
        self.win_img = pygame.image.load(get_resource_path("utils/Congrat.PNG"))
        self.load_next_country()

    def init_pygame(self) -> None:
        """
        Initiatiates pygame with clock and window caption
        """

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags with Capitals")

    def is_finished(self) -> bool:
        """
        Checks if all flags are guessed correctly
        """

        if len(self.checked_countries) == len(self.flags.flag_list):
            self.flags.current_flag_img = None
            self.finished = True
            return True
        else:
            return False

    def load_next_country(self) -> None:
        """
        Loads a scaled random flag
        Sets as current answer
        """

        self.flags.load_random_flag(self.checked_countries)
        self.capitals.set_current_answer(self.flags.current_flag_name)

    def event_handler(self) -> None:
        """
        Handles exit, input, buttons
        """

        for event in pygame.event.get():
            # Handle exit
            if event.type == pygame.QUIT:
                self.running = False

            input_text = self.input_box.event_handler(event)
            if input_text and not self.flags.shown:
                correct_flag = self.flags.check_answer(input_text)
                if correct_flag:
                    if self.capitals.current_capital is not None:
                        self.capitals.shown = True
                    else:
                        self.checked_countries.append(self.flags.current_flag_name)
                    self.flags.shown = True

            capital_result = self.capitals.event_handler(event)
            if capital_result:
                self.checked_countries.append(self.flags.current_flag_name)

            if self.next_button.is_clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
            ):
                if not self.is_finished():
                    self.load_next_country()
                    self.input_box.set_active()
                    self.flags.shown = False
                    self.capitals.shown = False

            if self.show_button.is_clicked(event) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_F1
            ):
                self.flags.answer_label.reveal()
                self.input_box.set_active()
                self.flags.shown = True

    def display_win(self) -> None:
        """
        Displays win image and label
        """

        self.flags.answer_label.set_answer("All countries are completed")
        self.flags.answer_label.reveal()
        self.display_image(self.win_img)

    def display_image(self, image: pygame.Surface) -> None:
        """
        Displays image in container
        Special rule for answer label on win
        """

        rect = image.get_rect(center=self.flags.image_container.center)
        self.screen.blit(image, rect)

        if self.finished:
            self.flags.answer_label_y_pos = rect.bottom + 60

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
            self.counter.draw(
                self.screen, len(self.checked_countries), len(self.flags.flag_list)
            )

            if self.flags.current_flag_img:
                self.display_image(self.flags.current_flag_img)

            if self.capitals.shown:
                self.capitals.draw(self.screen)

        self.flags.answer_label.draw(
            self.screen, self.width // 2, self.flags.answer_label_y_pos
        )

        pygame.display.flip()

    def main_loop(self) -> None:
        """
        Main logic wrapped here
        """

        while self.running:
            self.event_handler()
            self.update()


game = Game()
game.main_loop()
