import pygame
import json

from enemy import Enemy
from menu import MainMenu, CreditsMenu, PauseMenu
from logger import AdvancedLogger
from player import Player
from perk import CritRatePerk, CritDmgPerk, LootBonusPerk, DamageBonusPerk


class Game:
    """
    Класс, представляющий игру Enemy Clicker.

    Attributes:
        DISPLAY_WIDTH (int): Ширина окна игры.
        DISPLAY_HEIGHT (int): Высота окна игры.
        display (pygame.Surface): Поверхность для рисования игры.
        window (pygame.Surface): Окно игры.
        clock (pygame.time.Clock): Часы для контроля скорости игры.
        font_name (str): Путь к файлу шрифта.
        BLACK (pygame.Color): Черный цвет.
        WHITE (pygame.Color): Белый цвет.
        YELLOW (pygame.Color): Желтый цвет.
        GREEN (pygame.Color): Зеленый цвет.
        playing (bool): Флаг, определяющий, идет ли игра в данный момент.
        main_menu (MainMenu): Главное меню игры.
        credits_menu (CreditsMenu): Меню с кредитами.
        pause_menu (PauseMenu): Меню паузы игры.
        curr_menu (Menu): Текущее активное меню.
        ESCAPE (bool): Флаг, определяющий, была ли нажата клавиша ESC.
        CLICK (bool): Флаг, определяющий, была ли произведена левая кнопка мыши.
        player (Player): Объект игрока.
        enemy (Enemy): Объект противника.
        crit_rate_perk (CritRatePerk): Перк увеличения шанса критического удара.
        crit_dmg_perk (CritDmgPerk): Перк увеличения урона критического удара.
        loot_bonus_perk (LootBonusPerk): Перк увеличения добычи.
        damage_bonus_perk (DamageBonusPerk): Перк увеличения урона.
        shop_buttons (list): Список кнопок магазина.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    def __init__(self):
        """
        Инициализация объекта класса Game.

        Returns:
            None
        """
        pygame.init()
        self.DISPLAY_WIDTH = 800
        self.DISPLAY_HEIGHT = 500
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("Enemy Clicker")
        self.window = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_name = "Fonts/8-BIT WONDER.TTF"
        self.BLACK = pygame.Color(0, 0, 0)
        self.WHITE = pygame.Color(255, 255, 255)
        self.YELLOW = pygame.Color(255, 255, 0)
        self.GREEN = pygame.Color(0, 255, 0)
        self.playing = False
        self.main_menu = MainMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.curr_menu = self.main_menu
        self.ESCAPE = False
        self.CLICK = False

        pygame.mixer.music.load("Sounds/Ambient Dungeon.mp3")
        self.click_sound = pygame.mixer.Sound("Sounds/click_sound_1.mp3")
        self.click_sound.set_volume(0.3)

        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.player = Player(
            loot=0,
            loot_bonus=0,
            base_damage=1,
            critical_damage=1,
            critical_rate=0
        )

        self.enemy = Enemy(
            position=(self.DISPLAY_WIDTH // 2 - 20, self.DISPLAY_HEIGHT // 2 + 50)
        )

        self.crit_rate_perk = CritRatePerk()
        self.crit_dmg_perk = CritDmgPerk()
        self.loot_bonus_perk = LootBonusPerk()
        self.damage_bonus_perk = DamageBonusPerk()

        self.shop_buttons = []

        self.logger = AdvancedLogger(__name__)

    def run(self):
        """
        Запуск игры.

        Returns:
            None
        """
        while True:
            self.curr_menu.display_menu()
            if self.curr_menu == self.main_menu and self.playing:
                self.game_loop()

    def game_loop(self):
        """
        Главный игровой цикл.

        Returns:
            None
        """
        self.playing = True
        while self.playing:
            self.check_events()
            if self.ESCAPE:
                self.curr_menu = self.pause_menu
                self.curr_menu.display_menu()
            self.display.fill(self.BLACK)

            if self.CLICK:
                mouse_pos = pygame.mouse.get_pos()
                self.check_button_events(mouse_pos)
                self.player.click(mouse_pos, self.enemy, self)

            self.enemy.update()
            self.draw_info_box()
            self.draw_shop_box()

            self.window.blit(self.display, (0, 0))
            self.enemy.draw(self)
            pygame.display.update()
            self.clock.tick(60)

    def check_events(self):
        """
        Проверяет события pygame и обрабатывает нажатия клавиш и кнопок мыши.

        Returns:
            None
        """
        self.reset_keys()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.save_game()
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE = True
                    self.logger.debug("Button ESC was pressed.")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.CLICK = True
                    self.logger.debug("Mouse button was clicked.")
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.CLICK = False

    def quit(self):
        """
        Выход из игры.

        Returns:
            None
        """
        pygame.quit()
        quit()

    def reset_keys(self):
        """
        Сбрасывает значения флагов клавиш и кнопок мыши.

        Returns:
            None
        """
        self.ESCAPE = False
        self.CLICK = False

    def draw_text(self, text, size, x, y, color, alpha=255, align="center"):
        """
        Рисует текст на поверхности игры.

        Args:
            text (str): Текст для отображения.
            size (int): Размер шрифта.
            x (int): Координата x для позиционирования текста.
            y (int): Координата y для позиционирования текста.
            color (pygame.Color): Цвет текста.
            alpha (int, optional): Прозрачность текста (0-255). По умолчанию 255.
            align (str, optional): Выравнивание текста. "center" (по умолчанию), "left", "right".

        Returns:
            None
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect()

        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.topleft = (x, y)
        elif align == "right":
            text_rect.topright = (x, y)

        self.display.blit(text_surface, text_rect)

    def get_perks(self):
        """
        Возвращает список доступных перков.

        Returns:
            list: Список перков.
        """
        return [self.crit_rate_perk, self.crit_dmg_perk, self.loot_bonus_perk, self.damage_bonus_perk]

    def draw_shop_box(self):
        """
        Рисует окно магазина и отображает доступные перки.

        Returns:
            None
        """
        shop_box_width = 200
        shop_box_height = self.DISPLAY_HEIGHT - 100
        shop_box_x = self.DISPLAY_WIDTH - shop_box_width - 30
        shop_box_y = 50

        pygame.draw.rect(
            self.display,
            self.WHITE,
            (shop_box_x, shop_box_y, shop_box_width, shop_box_height)
        )
        pygame.draw.rect(
            self.display,
            self.BLACK,
            (shop_box_x + 2, shop_box_y + 2, shop_box_width - 4, shop_box_height - 4)
        )

        perks = self.get_perks()
        perk_height = 60
        perk_spacing = 100
        perk_x = shop_box_x + 20
        perk_y = shop_box_y + 7

        for perk in perks:
            pygame.draw.rect(
                self.display,
                self.WHITE,
                (perk_x, perk_y, shop_box_width - 40, perk_height)
            )
            pygame.draw.rect(
                self.display,
                self.BLACK,
                (perk_x + 2, perk_y + 2, shop_box_width - 44, perk_height - 4)
            )

            perk_name = perk.name.upper()
            perk_bonus = f"Bonus * {perk.get_bonus()}"
            perk_price = f"Price * {perk.get_price()}"

            self.draw_text(perk_name, 14, perk_x + 80, perk_y + 15, self.WHITE)
            self.draw_text(perk_bonus, 10, perk_x + 80, perk_y + 35, self.WHITE, align="center")
            self.draw_text(perk_price, 10, perk_x + 80, perk_y + 45, self.WHITE, align="center")

            buy_button_x = perk_x + 50
            buy_button_y = perk_y + 65
            buy_button_width = 60
            buy_button_height = 20

            pygame.draw.rect(
                self.display,
                self.YELLOW,
                (buy_button_x, buy_button_y, buy_button_width, buy_button_height)
            )
            pygame.draw.rect(
                self.display,
                self.BLACK,
                (buy_button_x + 2, buy_button_y + 2, buy_button_width - 4, buy_button_height - 4)
            )

            self.draw_text("BUY", 12, buy_button_x + buy_button_width // 2, buy_button_y + buy_button_height // 2,
                           self.YELLOW, align="center")

            self.shop_buttons.append((buy_button_x, buy_button_y, buy_button_width, buy_button_height, perk))

            perk_y += perk_spacing

    def check_button_events(self, mouse_pos):
        """
        Проверяет события кнопок магазина и выполняет соответствующие действия при нажатии.

        Args:
            mouse_pos (tuple): Координаты положения курсора мыши (x, y).

        Returns:
            None
        """
        for button in self.shop_buttons:
            x, y, width, height, perk = button
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                self.buy_perk(perk)
                break

    def buy_perk(self, perk):
        """
        Покупает выбранный перк и применяет его к игроку.

        Args:
            perk (Perk): Перк для покупки.

        Returns:
            None
        """
        if self.player.loot >= perk.get_price():
            self.player.loot -= perk.get_price()
            perk.apply(self.player)
            self.shop_buttons = []  # Очистить кнопки магазина после покупки

    def draw_info_box(self):
        """
        Рисует информационное окно и отображает информацию о состоянии игрока.

        Returns:
            None
        """
        info_width = 155
        info_height = 200
        info_x = 30
        info_y = self.DISPLAY_HEIGHT // 2 - info_height // 2

        pygame.draw.rect(
            self.display,
            self.WHITE,
            (info_x, info_y, info_width, info_height)
        )
        pygame.draw.rect(
            self.display,
            self.BLACK,
            (info_x + 2, info_y + 2, info_width - 4, info_height - 4)
        )

        info_lines = [
            f"LOOT * {self.player.loot}",
            f"LB * {self.player.loot_bonus}",
            f"DMG * {self.player.base_damage}",
            f"CR * {self.player.critical_rate}",
            f"CD * {self.player.critical_damage}"
        ]

        line_height = 30
        total_text_height = line_height * len(info_lines)
        text_x = info_x + info_width // 2
        text_y = info_y + (info_height - total_text_height) // 2

        for index, line in enumerate(info_lines):
            self.draw_text(line, 12, text_x, text_y, self.WHITE)
            text_y += line_height
            if index < len(info_lines) - 1:
                text_y += 5

    def save_game(self):
        """
        Сохраняет текущее состояние игры в файл.

        Returns:
            None
        """
        data = {
            "player": self.player.serialize(),
            "enemy": self.enemy.serialize(),
            "cr": self.crit_rate_perk.serialize(),
            "cd": self.crit_dmg_perk.serialize(),
            "ld": self.loot_bonus_perk.serialize(),
            "db": self.damage_bonus_perk.serialize(),
        }
        with open("save.json", "w") as f:
            json.dump(data, f, indent=2)
        self.logger.info("Game saved.")

    def load_game(self):
        """
        Загружает сохраненное состояние игры из файла.

        Returns:
            None
        """
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
                self.enemy.deserialize(data["enemy"])
                self.player.deserialize(data['player'])
                self.crit_rate_perk.deserialize(data['cr'])
                self.crit_dmg_perk.deserialize(data['cd'])
                self.loot_bonus_perk.deserialize(data['ld'])
                self.damage_bonus_perk.deserialize(data['db'])
            self.logger.info(f"Game loaded.")
        except FileNotFoundError:
            self.logger.error("File save.json not found.")

    def check_saved_game(self):
        """
        Проверяет наличие сохраненной игры.

        Returns:
            bool: True, если сохраненная игра существует, False в противном случае.
        """
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return False
        return True

