import pygame
from logger import AdvancedLogger


class Menu:
    """
    Класс, представляющий меню игры.

    Attributes:
        game (Game): Игровой объект.
        middle_width (int): Середина ширины экрана.
        middle_height (int): Середина высоты экрана.
        run_display (bool): Флаг для отображения меню.
        cursor_rect (pygame.Rect): Прямоугольник курсора.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self, game):
        """
        Инициализация объекта класса Menu.

        Args:
            game (Game): Игровой объект.

        Returns:
            None
        """
        self.game = game
        self.middle_width, self.middle_height = self.game.DISPLAY_WIDTH / 2, self.game.DISPLAY_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.logger = AdvancedLogger(__name__)

    def draw_cursor(self):
        """
        Отрисовка курсора.

        Returns:
            None
        """
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y, self.game.WHITE)

    def blit_screen(self):
        """
        Отрисовка экрана.

        Returns:
            None
        """
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class Button:
    """
    Класс, представляющий кнопку.

    Attributes:
        game (Game): Игровой объект.
        text (str): Текст на кнопке.
        x (int): Координата x кнопки.
        y (int): Координата y кнопки.
        width (int): Ширина кнопки.
        height (int): Высота кнопки.
        rect (pygame.Rect): Прямоугольник кнопки.
        is_selected (bool): Флаг выбора кнопки.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self, game, text, x, y):
        """
        Инициализация объекта класса Button.

        Args:
            game (Game): Игровой объект.
            text (str): Текст на кнопке.
            x (int): Координата x кнопки.
            y (int): Координата y кнопки.

        Returns:
            None
        """
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.width = 270
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_selected = False
        self.logger = AdvancedLogger(__name__)

    def draw(self):
        """
        Отрисовка кнопки.

        Returns:
            None
        """
        self.game.draw_text(self.text, 20, self.x + self.width / 2, self.y + self.height / 2, self.game.WHITE)

    def is_clicked(self, pos):
        """
        Проверка, была ли произведена клик мышью на кнопку.

        Args:
            pos (tuple): Позиция клика мыши.

        Returns:
            bool: Результат проверки клика на кнопку.
        """
        result = self.rect.collidepoint(pos)
        return result

    def __str__(self) -> str:
        """
        Возвращает текст кнопки.

        Returns:
            str: Текст кнопки.
        """
        return f"{self.text}"


class MainMenu(Menu):
    """
    Класс, представляющий главное меню игры.

    Attributes:
        game (Game): Игровой объект.
        state (str): Состояние меню.
        start_button (Button): Кнопка "Start Game".
        continue_button (Button): Кнопка "Continue Game".
        credits_button (Button): Кнопка "Credits".
        buttons (list): Список всех кнопок в меню.
        selected_button (Button): Выбранная кнопка.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self, game):
        """
        Инициализация объекта класса MainMenu.

        Args:
            game (Game): Игровой объект.

        Returns:
            None
        """
        super().__init__(game)
        self.state = "Start"
        self.start_button = Button(game, "Start Game", self.middle_width - 135, self.middle_height)
        self.continue_button = Button(game, "Continue Game", self.middle_width - 135, self.middle_height + 45)
        self.credits_button = Button(game, "Credits", self.middle_width - 135, self.middle_height + 90)
        self.quit_button = Button(game, "Quit", self.middle_width - 135, self.middle_height + 135)
        self.buttons = [self.start_button, self.continue_button, self.credits_button, self.quit_button]
        self.selected_button = None
        self.logger = AdvancedLogger(__name__)

    def display_menu(self):
        """
        Отображение главного меню.

        Returns:
            None
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('* Main Menu *', 20, self.middle_width, self.middle_height - 60, self.game.WHITE)
            for button in self.buttons:
                if button.is_selected:
                    pygame.draw.rect(self.game.display, self.game.YELLOW, button.rect, 3)
                button.draw()
            self.blit_screen()

    def check_input(self):
        """
        Обработка ввода пользователя.

        Returns:
            None
        """
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.is_selected = True
                clicked = True
                self.selected_button = button
                self.logger.debug(f"Button :{button}: was selected.")
            else:
                button.is_selected = False

        if self.game.CLICK and clicked:
            if self.selected_button == self.start_button:
                self.game.playing = True
                self.run_display = False
            elif self.selected_button == self.continue_button:
                if self.game.check_saved_game():
                    self.game.load_game()
                    self.game.playing = True
                    self.run_display = False
            elif self.selected_button == self.credits_button:
                self.game.curr_menu = self.game.credits_menu
                self.run_display = False
            elif self.selected_button == self.quit_button:
                self.game.quit()
            self.logger.debug(f"Button :{self.selected_button}: actions was activated.")


class CreditsMenu(Menu):
    """
    Класс, представляющий меню с кредитами.

    Attributes:
        game (Game): Игровой объект.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self, game):
        """
        Инициализация объекта класса CreditsMenu.

        Args:
            game (Game): Игровой объект.

        Returns:
            None
        """
        super().__init__(game)
        self.logger = AdvancedLogger(__name__)

    def display_menu(self):
        """
        Отображение меню с кредитами.

        Returns:
            None
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('* Credits *', 20, self.middle_width, self.middle_height - 20, self.game.WHITE)
            self.game.draw_text(
                'Made by David R and Makar K',
                15,
                self.middle_width,
                self.middle_height + 30,
                self.game.WHITE
            )
            self.game.draw_text(
                'Press ESC',
                15,
                self.middle_width,
                self.middle_height + 70,
                self.game.WHITE,
                128
            )
            self.blit_screen()

    def check_input(self):
        """
        Обработка ввода пользователя.

        Returns:
            None
        """
        if self.game.ESCAPE:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
            self.logger.debug("Exiting.")


class PauseMenu(Menu):
    """
    Класс, представляющий меню паузы игры.

    Attributes:
        game (Game): Игровой объект.
        save_button (Button): Кнопка "Save Game".
        quit_button (Button): Кнопка "Quit".
        buttons (list): Список всех кнопок в меню.
        selected_button (Button): Выбранная кнопка.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self, game):
        """
        Инициализация объекта класса PauseMenu.

        Args:
            game (Game): Игровой объект.

        Returns:
            None
        """
        super().__init__(game)
        self.save_button = Button(game, "Save Game", self.middle_width - 135, self.middle_height + 10)
        self.quit_button = Button(game, "Quit", self.middle_width - 135, self.middle_height + 50)
        self.buttons = [self.save_button, self.quit_button]
        self.selected_button = self.save_button
        self.logger = AdvancedLogger(__name__)

    def display_menu(self):
        """
        Отображение меню паузы игры.

        Returns:
            None
        """
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('* Pause Menu *', 20, self.middle_width, self.middle_height - 60, self.game.WHITE)
            for button in self.buttons:
                if button.is_selected:
                    pygame.draw.rect(self.game.display, self.game.YELLOW, button.rect, 3)
                button.draw()
            self.blit_screen()

    def check_input(self):
        """
        Обработка ввода пользователя.

        Returns:
            None
        """
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.is_selected = True
                self.selected_button = button
                self.logger.debug(f"Button :{button}: was selected.")
            else:
                button.is_selected = False

        if self.game.CLICK:
            if self.selected_button == self.save_button:
                self.game.save_game()
            elif self.selected_button == self.quit_button:
                self.game.playing = False
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            self.logger.debug(f"Button :{self.selected_button}: actions was activated.")
