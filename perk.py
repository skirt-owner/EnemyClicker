from dataclasses import dataclass, asdict


@dataclass
class Perk:
    """
    Класс, представляющий перк.

    Attributes:
        name (str): Название перка.
        base_price (int): Базовая цена перка.
        base_bonus (int): Базовый бонус перка.
        price_scale (float): Масштабный коэффициент цены перка.
        bonus_scale (float): Масштабный коэффициент бонуса перка.
        level (int): Уровень перка.
    """

    name: str
    base_price: int
    base_bonus: int
    price_scale: float
    bonus_scale: float
    level: int

    def __init__(self, name, base_price, base_bonus, price_scale=1.2, bonus_scale=1) -> None:
        """
        Инициализация объекта класса Perk.

        Args:
            name (str): Название перка.
            base_price (int): Базовая цена перка.
            base_bonus (int): Базовый бонус перка.
            price_scale (float, optional): Масштабный коэффициент цены перка. По умолчанию 1.2.
            bonus_scale (float, optional): Масштабный коэффициент бонуса перка. По умолчанию 1.

        Returns:
            None
        """
        self.name = name
        self.base_price = base_price
        self.base_bonus = base_bonus
        self.price_scale = price_scale
        self.bonus_scale = bonus_scale
        self.level = 0

    def get_price(self) -> int:
        """
        Получает текущую цену перка.

        Returns:
            int: Текущая цена перка.
        """
        return int(self.base_price * (self.price_scale ** self.level))

    def get_bonus(self) -> int:
        """
        Получает текущий бонус перка.

        Returns:
            int: Текущий бонус перка.
        """
        return int(self.base_bonus + self.level * self.bonus_scale)

    def upgrade(self) -> None:
        """
        Повышает уровень перка на 1.

        Returns:
            None
        """
        self.level += 1

    def serialize(self) -> dict:
        """
        Сериализует объект перка.

        Returns:
            dict: Сериализованные данные объекта перка.
        """
        return asdict(self)

    def deserialize(self, data) -> None:
        """
        Десериализует объект перка из данных.

        Args:
            data (dict): Сериализованные данные объекта перка.

        Returns:
            None
        """
        for key, value in data.items():
            setattr(self, key, value)


@dataclass
class CritRatePerk(Perk):
    """
    Класс, представляющий перк увеличения шанса критического удара.
    Наследуется от класса Perk.

    Attributes:
        Inherits attributes from Perk.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта класса CritRatePerk.

        Returns:
            None
        """
        super().__init__("CR", 100, 1)

    def apply(self, player) -> None:
        """
        Применяет перк к игроку.

        Args:
            player (Player): Игрок, к которому применяется перк.

        Returns:
            None
        """
        player.critical_rate += self.get_bonus()
        self.upgrade()


@dataclass
class CritDmgPerk(Perk):
    """
    Класс, представляющий перк увеличения урона критического удара.
    Наследуется от класса Perk.

    Attributes:
        Inherits attributes from Perk.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта класса CritDmgPerk.

        Returns:
            None
        """
        super().__init__("CD", 50, 5)

    def apply(self, player) -> None:
        """
        Применяет перк к игроку.

        Args:
            player (Player): Игрок, к которому применяется перк.

        Returns:
            None
        """
        player.critical_damage += self.get_bonus()
        self.upgrade()


@dataclass
class LootBonusPerk(Perk):
    """
    Класс, представляющий перк увеличения бонуса к добыче.
    Наследуется от класса Perk.

    Attributes:
        Inherits attributes from Perk.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта класса LootBonusPerk.

        Returns:
            None
        """
        super().__init__("LB", 100, 2)

    def apply(self, player) -> None:
        """
        Применяет перк к игроку.

        Args:
            player (Player): Игрок, к которому применяется перк.

        Returns:
            None
        """
        player.loot_bonus += self.get_bonus()
        self.upgrade()


@dataclass
class DamageBonusPerk(Perk):
    """
    Класс, представляющий перк увеличения бонуса к урону.
    Наследуется от класса Perk.

    Attributes:
        Inherits attributes from Perk.
    """

    def __init__(self) -> None:
        """
        Инициализация объекта класса DamageBonusPerk.

        Returns:
            None
        """
        super().__init__("DB", 50, 5)

    def apply(self, player) -> None:
        """
        Применяет перк к игроку.

        Args:
            player (Player): Игрок, к которому применяется перк.

        Returns:
            None
        """
        player.base_damage += self.get_bonus()
        self.upgrade()
