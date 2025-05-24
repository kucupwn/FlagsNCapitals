import pygame

BLACK = (0, 0, 0)
COLOR_INACTIVE = (200, 200, 200)
COLOR_ACTIVE = (20, 20, 160)


class InputBox:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.font = pygame.font.Font(None, 36)
        self.input_box_width = 500
        self.input_box_height = 40
        self.input_box = pygame.Rect(
            (screen_width - self.input_box_width) // 2,
            screen_height * 0.08,
            self.input_box_width,
            self.input_box_height,
        )
        self.input_color = COLOR_ACTIVE
        self.input_active = True
        self.input_text = ""

    def add_search_label(self, screen: pygame.Surface) -> None:
        """
        Add label above input box
        """

        txt_surface = self.font.render("Type here:", True, BLACK)
        screen.blit(txt_surface, (self.input_box.x, self.input_box.y - 40))

    def event_handler(self, event: pygame.event.Event) -> None:
        """
        Handles input box events: active input box, input str, backspace, ctrl+backspace
        Returns after every event
        """

        # Click to activate the input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
                self.input_color = COLOR_ACTIVE
            elif not self.input_box.collidepoint(event.pos):
                self.input_active = False
                self.input_color = COLOR_INACTIVE

        # Handle typing
        if event.type == pygame.KEYDOWN and self.input_active:
            # Handle character deletion
            if event.key == pygame.K_BACKSPACE:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    self.input_text = self.input_text.rstrip()
                    self.input_text = " ".join(self.input_text.split()[:-1])
                else:
                    self.input_text = self.input_text[:-1]
            else:
                # Input any character
                self.input_text += event.unicode

            # Return for continous display
            return self.input_text.lower().strip()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw input box onto screen
        """

        txt_surface = self.font.render(self.input_text, True, BLACK)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(screen, self.input_color, self.input_box, 2)
