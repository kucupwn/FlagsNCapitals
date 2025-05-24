import pygame
from input_box import InputBox

BACKGROUND = (255, 255, 255)


class Flags:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.flags_dir = "flags"
        self.running = True

        self.init_pygame()
        self.input_box = InputBox(self.width, self.height)

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags")

    def event_handler(self):
        for event in pygame.event.get():
            # Handle exit
            if event.type == pygame.QUIT:
                self.running = False

            input_text = self.input_box.event_handler(event)
            if input_text:
                print(input_text)

    def update(self):
        self.clock.tick(60)
        self.screen.fill(BACKGROUND)
        self.input_box.add_search_label(self.screen)
        self.input_box.draw(self.screen)

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.event_handler()
            self.update()


game = Flags()
game.main_loop()
