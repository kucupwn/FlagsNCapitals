import pygame


class Flags:
    def __init__(self):
        self.width = 1280
        self.height = 720

        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flags")


game = Flags()
