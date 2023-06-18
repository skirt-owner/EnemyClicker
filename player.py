import random
from dataclasses import dataclass, asdict
from logger import AdvancedLogger


@dataclass
class Player:
    """
    Класс, представляющий игрока.

    Attributes:
        loot (int): Количество добычи игрока.
        loot_bonus (int): Бонус к добыче игрока.
        base_damage (int): Базовый урон игрока.
        critical_damage (int): Урон критического удара игрока.
        critical_rate (int): Шанс критического удара игрока.
        logger (AdvancedLogger): Логгер для записи информации.
    """

    loot: int
    loot_bonus: int
    base_damage: int
    critical_damage: int
    critical_rate: int

    def __init__(
            self,
            loot: int,
            loot_bonus: int,
            base_damage: int,
            critical_damage: int,
            critical_rate: int
    ) -> None:
        """
        Инициализация объекта класса Player.

        Args:
            loot (int): Количество добычи игрока.
            loot_bonus (int): Бонус к добыче игрока.
            base_damage (int): Базовый урон игрока.
            critical_damage (int): Урон критического удара игрока.
            critical_rate (int): Шанс критического удара игрока.

        Returns:
            None
        """
        self.loot = loot
        self.loot_bonus = loot_bonus
        self.base_damage = base_damage + 5
        self.critical_damage = critical_damage
        self.critical_rate = critical_rate
        self.logger = AdvancedLogger(__name__)

    def click(self, mouse_pos, enemy, game) -> None:
        """
        Обработка клика игрока.

        Args:
            mouse_pos (tuple): Позиция клика мыши.
            enemy (Enemy): Враг, по которому произведен клик.
            game (Game): Игровой объект.

        Returns:
            None
        """
        self.logger.debug(f"Игрок кликнул: {mouse_pos}")

        if enemy.rect.collidepoint(mouse_pos) and not enemy.is_dead:
            game.click_sound.play()
            enemy.play_click_animation()

            damage = self.calculate_damage()
            reward = enemy.hit(damage=damage)
            self.loot += self.calculate_reward(reward)

    def calculate_reward(self, reward) -> int:
        """
        Расчет награды игрока.

        Args:
            reward (float): Награда за попадание по врагу.

        Returns:
            int: Рассчитанная награда игрока.
        """
        reward *= (1 + self.loot_bonus / 100)
        return int(reward)

    def calculate_damage(self) -> int:
        """
        Расчет урона игрока.

        Returns:
            int: Рассчитанный урон игрока.
        """
        damage = self.base_damage
        if random.randint(0, 100) < self.critical_rate:
            damage *= (1 + self.critical_damage / 100)
        return int(damage)

    def serialize(self) -> dict:
        """
        Сериализация объекта игрока.

        Returns:
            dict: Сериализованный объект игрока.
        """
        return asdict(self)

    def deserialize(self, data) -> None:
        """
        Десериализация объекта игрока.

        Args:
            data (dict): Сериализованный объект игрока.

        Returns:
            None
        """
        for key, value in data.items():
            setattr(self, key, value)
