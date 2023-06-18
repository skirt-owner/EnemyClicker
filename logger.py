import logging
import inspect
from typing import Union


class ClassNameTrackingMeta(type):
    """
    Метакласс ClassNameTrackingMeta добавляет атрибут '__class_name__' к создаваемым классам,
    содержащий полное имя класса в формате 'модуль.класс'.

    :param type: Базовый метакласс
    """

    def __new__(mcs, name, bases, attrs) -> object:
        """
        Создает новый класс с добавленным атрибутом '__class_name__'.

        :param name: Имя класса
        :param bases: Базовые классы
        :param attrs: Атрибуты класса
        :return: Новый класс с добавленным '__class_name__'
        """
        attrs['__class_name__'] = f'{attrs.get("__module__", "")}.{name}'
        return super().__new__(mcs, name, bases, attrs)


def filter_duplicates(func):
    """
    Декоратор filter_duplicates проверяет, является ли сообщение дубликатом последнего залогированного сообщения.

    :param func: Декорируемая функция логирования
    :return: Обертка для функции логирования
    """

    def wrapper(self, message, *args, **kwargs) -> Union[None, func]:
        """
        Проверяет дублирование сообщения перед вызовом функции логирования.

        :param self: Экземпляр класса
        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        :return: Результат вызова функции логирования или None, если сообщение является дубликатом
        """
        if self.is_duplicated(message):
            return
        return func(self, message, *args, **kwargs)

    return wrapper


class Logger(logging.Logger, metaclass=ClassNameTrackingMeta):
    """
    Класс Logger расширяет функциональность стандартного класса logging.Logger.
    Он добавляет отслеживание имени класса, из которого происходит вызов логирования.

    :param name: Имя логгера
    :param level: Уровень логирования (по умолчанию DEBUG)
    """

    def __init__(self, name, level=logging.DEBUG):
        """
        Инициализация объекта логгера.

        :param name: Имя логгера
        :param level: Уровень логирования (по умолчанию DEBUG)
        """
        super().__init__(name, level)
        self.last_log_message = None

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter('%(levelname)s - %(class_name)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.addHandler(console_handler)

        file_handler = logging.FileHandler('game.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(class_name)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)

    def is_duplicated(self, message) -> bool:
        """
        Проверяет, является ли сообщение дубликатом последнего залогированного сообщения.

        :param message: Сообщение лога
        :return: True, если сообщение является дубликатом, False в противном случае
        """
        if message == self.last_log_message:
            return True
        self.last_log_message = message
        return False


def get_class_name():
    """
    Получает полное имя класса, из которого вызывается функция логирования.

    :return: Полное имя класса (модуль.класс) или имя класса, если модуль не найден
    """
    stack = inspect.stack()
    frame = next((frame for frame in stack[3:] if frame[0].f_locals.get('self', None)), None)
    module = inspect.getmodule(frame[0])
    class_name = frame[0].f_locals['self'].__class__.__name__ if frame else ''
    return f'{module.__name__}.{class_name}' if module else class_name


class AdvancedLogger(Logger):
    """
    Класс AdvancedLogger расширяет функциональность класса Logger.
    Он добавляет декоратор filter_duplicates для фильтрации дублирующихся сообщений в логах.

    :param Logger: Базовый класс логгера
    """

    @filter_duplicates
    def debug(self, message, *args, **kwargs) -> None:
        """
        Логирование сообщения уровня DEBUG.

        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        kwargs.setdefault('extra', {})['class_name'] = get_class_name()
        super().debug(message, *args, **kwargs)

    @filter_duplicates
    def info(self, message, *args, **kwargs) -> None:
        """
        Логирование сообщения уровня INFO.

        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        kwargs.setdefault('extra', {})['class_name'] = get_class_name()
        super().info(message, *args, **kwargs)

    @filter_duplicates
    def warning(self, message, *args, **kwargs) -> None:
        """
        Логирование сообщения уровня WARNING.

        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        kwargs.setdefault('extra', {})['class_name'] = get_class_name()
        super().warning(message, *args, **kwargs)

    @filter_duplicates
    def error(self, message, *args, **kwargs) -> None:
        """
        Логирование сообщения уровня ERROR.

        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        kwargs.setdefault('extra', {})['class_name'] = get_class_name()
        super().error(message, *args, **kwargs)

    @filter_duplicates
    def critical(self, message, *args, **kwargs) -> None:
        """
        Логирование сообщения уровня CRITICAL.

        :param message: Сообщение лога
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        kwargs.setdefault('extra', {})['class_name'] = get_class_name()
        super().critical(message, *args, **kwargs)
