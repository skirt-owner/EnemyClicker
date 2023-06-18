import glob
import random

import pygame
from dataclasses import dataclass, asdict

from pygame import Surface

from logger import AdvancedLogger


@dataclass
class Enemy:
    """
    Класс, представляющий вражеский персонаж в игре.
    """
    base_health: int
    health: int
    base_health_increase: int
    base_health_growth_rate: float
    base_health_growth_factor: float
    enemy_count: int

    def __init__(self, position):
        """
        Инициализирует атрибуты врага.

        Args:
            position (tuple): Начальная позиция врага.
        """

        self.levels = 7                    # Уровни врага.
        self.enemy_count = 0               # Количество врагов данного типа, посчитанное с начала игры.
        self.position = position           # Позиция врага на экране.
        self.death_frames = self.load_death_frames()      # Список кадров анимации смерти врага.
        self.idle_frames = self.load_idle_frames()        # Список кадров анимации покоя врага.
        self.current_animation = self.idle_frames         # Текущая анимация врага.
        self.current_frame_index = 0       # Индекс текущего кадра анимации.
        self.animation_speed = 0.1         # Скорость анимации врага.
        self.animation_timer = 0           # Таймер для контроля скорости анимации.
        self.size = (250, 250)             # Размер врага.
        self.rect = pygame.Rect(
            self.position[0],
            self.position[1],
            self.size[0],
            self.size[1]
        )                                 # Прямоугольник, определяющий границы врага на экране.
        self.original_size = self.size     # Начальный размер врага.
        self.shrink_duration = 0.1         # Продолжительность уменьшения размера врага.
        self.grow_duration = 0.1           # Продолжительность увеличения размера врага.
        self.shrink_timer = 0              # Таймер уменьшения размера врага.
        self.grow_timer = 0                # Таймер увеличения размера врага.
        self.is_shrinking = False          # Флаг, указывающий, происходит ли уменьшение размера врага.
        self.is_growing = False            # Флаг, указывающий, происходит ли увеличение размера врага.
        self.base_health = 10              # Базовое здоровье врага.
        self.health = self.base_health     # Текущее здоровье врага.
        self.is_dead = False               # Флаг, указывающий, мертв ли враг.
        self.base_health_increase = 5      # Количество увеличения здоровья при повышении уровня.
        self.base_health_growth_rate = 0.2 # Скорость роста базового здоровья при повышении уровня.
        self.base_health_growth_factor = 1.0 # Множитель роста базового здоровья при повышении уровня.

        self.logger = AdvancedLogger(__name__)

    def hit(self, damage):
        """
        Обрабатывает попадание врага под атаку.

        Args:
            damage (int): Урон, нанесенный врагу.

        Returns:
            int: Количество добычи, выпавшей из врага после его смерти, или 0, если враг все еще жив.
        """

        self.health -= damage
        if self.health <= 0:
            return self.calculate_loot_count()
        return 0

    def calculate_loot_count(self):
        """
        Рассчитывает количество добычи, выпавшей из врага после его смерти.

        Returns:
            int: Количество добычи.
        """

        scaling_factor = 1 / (self.base_health ** 0.5)
        loot_count = int(self.base_health * scaling_factor * random.uniform(0.8, 1.2))

        return loot_count

    def reset_health(self):
        """
        Сбрасывает здоровье врага до его базового значения, и устанавливает флаг "мертвый" в False.
        """

        self.is_dead = False
        self.play_idle_animation()
        self.health = self.base_health

    def increase_health(self):
        """
        Увеличивает базовое здоровье врага на основе множителя роста здоровья.
        """

        self.base_health += round(self.base_health_increase * self.base_health_growth_factor)

    def load_idle_frames(self):
        """
        Загружает кадры анимации покоя врага из соответствующей директории.

        Returns:
            list: Список кадров анимации покоя.
        """

        frames = []
        directory = f"Images/Enemy/{self.enemy_count % self.levels}"
        idle_file_pattern = f"idle*.png"
        idle_frame_names = glob.glob(directory + "/" + idle_file_pattern)
        for name in idle_frame_names:
            frame = pygame.image.load(name).convert_alpha()
            frames.append(frame)
        return frames

    def load_death_frames(self):
        """
        Загружает кадры анимации смерти врага из соответствующей директории.

        Returns:
            list: Список кадров анимации смерти.
        """

        frames = []
        directory = f"Images/Enemy/{self.enemy_count % self.levels}"
        death_file_pattern = f"death*.png"
        death_frame_names = glob.glob(directory + "/" + death_file_pattern)
        for name in death_frame_names:
            frame = pygame.image.load(name).convert_alpha()
            frames.append(frame)
        return frames

    def update_frames(self):
        """
        Обновляет списки кадров анимации покоя и смерти врага.

        Note:
            Метод использует текущее значение атрибута self.enemy_count.

        """
        self.idle_frames = []
        self.death_frames = []

        directory = f"Images/Enemy/{self.enemy_count % self.levels}"
        idle_file_pattern = f"idle*.png"
        death_file_pattern = f"death*.png"

        idle_frame_names = glob.glob(directory + "/" + idle_file_pattern)
        death_frame_names = glob.glob(directory + "/" + death_file_pattern)

        for name in idle_frame_names:
            frame = pygame.image.load(name).convert_alpha()
            self.idle_frames.append(frame)

        for name in death_frame_names:
            frame = pygame.image.load(name).convert_alpha()
            self.death_frames.append(frame)

    def play_click_animation(self):
        """
        Воспроизводит анимацию нажатия на врага.

        Note:
            Если текущая анимация врага - анимация покоя, то сбрасывает индекс текущего кадра, таймер анимации
            и устанавливает флаги уменьшения размера и таймера уменьшения размера врага.
        """

        if self.current_animation == self.idle_frames:
            self.current_frame_index = 0
            self.animation_timer = 0
            self.is_shrinking = True
            self.shrink_timer = 0

    def play_death_animation(self):
        """
        Воспроизводит анимацию смерти врага.

        Note:
            Если текущая анимация врага не является анимацией смерти, то устанавливает текущую анимацию
            как анимацию смерти, сбрасывает индекс текущего кадра и таймер анимации.
        """

        if self.current_animation != self.death_frames:
            self.current_animation = self.death_frames
            self.current_frame_index = 0
            self.animation_timer = 0

    def play_idle_animation(self):
        """
        Воспроизводит анимацию покоя врага.

        Note:
            Если текущая анимация врага не является анимацией покоя, то устанавливает текущую анимацию
            как анимацию покоя, сбрасывает индекс текущего кадра и таймер анимации, а также сбрасывает флаги уменьшения
            размера и увеличения размера врага и восстанавливает оригинальный размер врага.
        """

        if self.current_animation != self.idle_frames:
            self.current_animation = self.idle_frames
            self.current_frame_index = 0
            self.animation_timer = 0
            self.is_shrinking = False
            self.is_growing = False
            self.size = self.original_size

    def update(self) -> None:
        """
        Обновляет состояние врага и его анимацию.

        Note:
            Метод обрабатывает смерть врага, изменение размера врага, обновление анимации,
            вычисление скорости анимации в зависимости от количества кадров, а также обновление прямоугольника
            области врага на основе его позиции и размера.

        Returns:
            None
        """

        if self.health <= 0 and not self.is_dead:
            self.enemy_count += 1
            self.is_dead = True
            self.play_death_animation()

        if self.is_dead:
            if self.current_frame_index == len(self.current_animation) - 1:
                self.update_frames()
                self.base_health_growth_factor += self.base_health_growth_rate
                self.increase_health()
                self.reset_health()
                self.play_idle_animation()
                return

        if self.is_shrinking:
            self.shrink_timer += 0.01
            self.size = (
                int(self.original_size[0] * (1 - self.shrink_timer / self.shrink_duration)),
                int(self.original_size[1] * (1 - self.shrink_timer / self.shrink_duration))
            )
            if self.shrink_timer >= self.shrink_duration:
                self.is_shrinking = False
                self.is_growing = True
                self.grow_timer = 0

        if self.is_growing:
            self.grow_timer += 0.01
            self.size = (
                int(self.original_size[0] * (self.grow_timer / self.grow_duration)),
                int(self.original_size[1] * (self.grow_timer / self.grow_duration))
            )
            if self.grow_timer >= self.grow_duration:
                self.is_growing = False
                self.size = self.original_size

        self.rect = pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )

        self.animation_timer += 0.01
        if self.animation_timer >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_animation)
            self.animation_timer = 0

        num_frames = len(self.current_animation)
        min_speed = 0.02
        max_speed = 0.2
        threshold_frames = 5

        if num_frames > threshold_frames:
            speed_range = max_speed - min_speed
            adjusted_speed = (num_frames - threshold_frames) / num_frames * speed_range
            self.animation_speed = max_speed - adjusted_speed
        else:
            self.animation_speed = max_speed

    def draw(self, game) -> None:
        """
        Отрисовывает врага на игровом окне, включая текущий кадр анимации и полоску здоровья.

        Args:
            game (Game): Игра, на которой происходит отрисовка.

        Returns:
            None
        """

        current_frame = self.current_animation[self.current_frame_index]
        frame = pygame.transform.scale(current_frame, self.size)
        frame_rect = frame.get_rect(center=self.position)
        game.window.blit(frame, frame_rect)

        health_bar_width = 150
        health_bar_height = 22
        health_bar_x = self.position[0] - self.original_size[0] // 2 + 60
        health_bar_y = self.position[1] - self.original_size[1] // 2 - health_bar_height

        background_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(game.window, (50, 50, 50), background_rect, border_radius=health_bar_height // 2)

        filled_width = int((self.health / self.base_health) * (health_bar_width - 4))
        filled_width = max(0, min(filled_width, health_bar_width - 4))

        gradient_start_color = (220, 20, 60)
        gradient_end_color = (255, 69, 0)
        gradient_rect = pygame.Rect(
            health_bar_x + 2,
            health_bar_y + 2,
            filled_width,
            health_bar_height - 4
        )
        pygame.draw.rect(
            game.window,
            gradient_start_color,
            gradient_rect,
            border_radius=(health_bar_height - 4) // 2
        )
        pygame.draw.rect(
            game.window,
            gradient_end_color,
            gradient_rect,
            3,
            border_radius=(health_bar_height - 4) // 2
        )

        text_x = health_bar_x + health_bar_width // 2
        text_y = health_bar_y + health_bar_height // 2

        font = pygame.font.Font(game.font_name, 12)

        if not self.is_dead:
            text_surface = font.render(f"{self.health}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            game.window.blit(text_surface, text_rect)
        else:
            dead_text = font.render("DEAD", True, (255, 0, 0))
            dead_text_rect = dead_text.get_rect(center=(text_x, text_y))
            game.window.blit(dead_text, dead_text_rect)

    def serialize_surface(self, surface) -> dict:
        """
        Сериализует поверхность Pygame.

        Args:
            surface (Surface): Поверхность Pygame.

        Returns:
            dict: Сериализованные данные о поверхности.
        """

        width, height = surface.get_size()
        image_str = pygame.image.tostring(surface, 'RGBA').decode('latin-1')

        serialized_surface = {
            'width': width,
            'height': height,
            'image': image_str
        }

        return serialized_surface

    def serialize_frames(self, frames) -> list:
        """
        Сериализует список кадров анимации.

        Args:
            frames (list): Список кадров анимации (поверхностей Pygame).

        Returns:
            list: Сериализованные данные о кадрах анимации.
        """

        serialized_frames = []
        for frame in frames:
            serialized_frame = self.serialize_surface(frame)
            serialized_frames.append(serialized_frame)

        return serialized_frames

    def serialize(self) -> dict:
        """
        Сериализует объект врага.

        Returns:
            dict: Сериализованные данные объекта врага.
        """

        serialized_idle_frames = self.serialize_frames(self.idle_frames)
        serialized_death_frames = self.serialize_frames(self.death_frames)

        serialized_data = asdict(self)
        serialized_data['idle_frames'] = serialized_idle_frames
        serialized_data['death_frames'] = serialized_death_frames

        return serialized_data

    def deserialize_surface(self, serialized_surface) -> Surface:
        """
        Десериализует поверхность Pygame.

        Args:
            serialized_surface (dict): Сериализованные данные о поверхности.

        Returns:
            Surface: Восстановленная поверхность Pygame.
        """

        width = serialized_surface['width']
        height = serialized_surface['height']
        image_str = serialized_surface['image']
        image_data = pygame.image.fromstring(image_str.encode('latin-1'), (width, height), 'RGBA')

        return image_data

    def deserialize_frames(self, serialized_frames) -> list:
        """
        Десериализует список кадров анимации.

        Args:
            serialized_frames (list): Сериализованные данные о кадрах анимации.

        Returns:
            list: Восстановленные кадры анимации (поверхности Pygame).
        """

        frames = []
        for serialized_frame in serialized_frames:
            frame = self.deserialize_surface(serialized_frame)
            frames.append(frame)

        return frames

    def deserialize(self, data) -> None:
        """
        Десериализует объект врага из данных.

        Args:
            data (dict): Сериализованные данные объекта врага.

        Returns:
            None
        """

        for key, value in data.items():
            if key == 'idle_frames':
                self.idle_frames = self.deserialize_frames(value)
            elif key == 'death_frames':
                self.death_frames = self.deserialize_frames(value)
            else:
                setattr(self, key, value)

        if self.is_dead:
            self.current_animation = self.death_frames
        else:
            self.current_animation = self.idle_frames
