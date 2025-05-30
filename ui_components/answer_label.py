import pygame


class AnswerLabel:
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 64)
        self.revealed = False

    def set_answer(self, answer: str) -> None:
        """
        Sets current answer
        Converts it to title case
        """

        self.revealed = False
        self.answer_text = answer.title()

    def reveal(self) -> None:
        """
        Toggles answer displaying
        """

        self.revealed = True

    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Sets text to unknown or answer
        Draws on screens
        """

        text = self.answer_text if self.revealed else "???"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
