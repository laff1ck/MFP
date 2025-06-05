import pygame
import os
import sys
from pygame.locals import *


class CorridorSimulator:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Симулятор движения по коридору")

        # Инициализация шрифта
        self.font = pygame.font.SysFont('Arial', 20)

        # Начальные настройки
        self.position = [0, 0]  # Текущая позиция (x, y)
        self.direction = 4  # Начальное направление (180°)
        self.step_size = 1  # Шаг движения

        # Загрузка изображений
        self.image_database = self.load_images()
        self.update_image()

    def load_images(self):
        """Загружает изображения и создает структуру данных для быстрого доступа"""
        image_db = {}

        # Проверяем наличие папки с изображениями
        if not os.path.exists('corridor_images'):
            os.makedirs('corridor_images')
            print("Создана папка 'corridor_images'. Добавьте изображения в формате x_0_angle.jpg")

        try:
            # Загружаем изображения для 3 позиций (0,1,2) и 8 направлений
            for x in range(3):
                for angle in range(0, 360, 45):
                    filename = f"corridor_images/{x}_0_{angle}.jpg"
                    if os.path.exists(filename):
                        image = pygame.image.load(filename)
                        image = pygame.transform.scale(image, (self.width, self.height))
                        image_db[(x, 0, angle)] = image
                    else:
                        # Создаем заглушку
                        surf = pygame.Surface((self.width, self.height))
                        color = (100, 100, 100) if angle == 180 else (50, 50, 50)
                        surf.fill(color)
                        text = self.font.render(f"X: {x} Angle: {angle}°", True, (255, 255, 255))
                        surf.blit(text, (50, 50))
                        image_db[(x, 0, angle)] = surf
            return image_db
        except Exception as e:
            print(f"Ошибка загрузки изображений: {e}")
            return {}

    def update_image(self):
        """Обновляет текущее изображение"""
        key = (self.position[0], 0, self.direction * 45)
        self.current_image = self.image_database.get(key, None)

        if self.current_image is None:
            # Создаем заглушку для отсутствующего изображения
            self.current_image = pygame.Surface((self.width, self.height))
            self.current_image.fill((50, 50, 50))
            text = self.font.render(f"Нет изображения: X={self.position[0]}, Угол={self.direction * 45}°",
                                    True, (255, 255, 255))
            self.current_image.blit(text, (50, 50))

    def move_forward(self):
        """Движение вперед с учетом специальных правил"""
        new_pos = self.position.copy()

        # Правила для направления 180°
        if self.direction == 4:
            if self.position[0] == 0:  # Из 0_0_180 можно идти только вперед в 1_0_180
                new_pos[0] = 1
            elif self.position[0] == 1:  # Из 1_0_180 можно идти вперед в 2_0_180
                new_pos[0] = 2
            elif self.position[0] == 2:  # В 2_0_180 нельзя идти вперед
                return

        # Правила для направления 0°
        elif self.direction == 0:
            if self.position[0] == 0:  # Из 0_0_0 можно идти назад в 1_0_0
                new_pos[0] = 1
            elif self.position[0] == 1:  # Из 1_0_0 можно идти вперед в 0_0_0 или назад в 2_0_0
                new_pos[0] = 2
            elif self.position[0] == 2:  # В 2_0_0 нельзя идти вперед
                return

        self.position = new_pos
        self.update_image()

    def move_backward(self):
        """Движение назад с учетом специальных правил"""
        new_pos = self.position.copy()

        # Правила для направления 180°
        if self.direction == 4:
            if self.position[0] == 0:  # В 0_0_180 нельзя идти назад
                return
            elif self.position[0] == 1:  # Из 1_0_180 можно идти назад в 0_0_180
                new_pos[0] = 0
            elif self.position[0] == 2:  # Из 2_0_180 можно идти назад в 1_0_180
                new_pos[0] = 1

        # Правила для направления 0°
        elif self.direction == 0:
            if self.position[0] == 0:  # В 0_0_0 нельзя идти вперед (это move_forward)
                return
            elif self.position[0] == 1:  # Из 1_0_0 можно идти назад в 0_0_0
                new_pos[0] = 0
            elif self.position[0] == 2:  # Из 2_0_0 можно идти назад в 1_0_0
                new_pos[0] = 1

        self.position = new_pos
        self.update_image()

    def turn_left(self):
        """Поворот налево на 45°"""
        self.direction = (self.direction - 1) % 8
        self.update_image()

    def turn_right(self):
        """Поворот направо на 45°"""
        self.direction = (self.direction + 1) % 8
        self.update_image()

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_UP:
                    self.move_forward()
                elif event.key == K_DOWN:
                    self.move_backward()
                elif event.key == K_LEFT:
                    self.turn_left()
                elif event.key == K_RIGHT:
                    self.turn_right()
        return True

    def draw_info(self):
        """Отображает информацию"""
        info_text = f"Позиция: X={self.position[0]} | Угол: {self.direction * 45}°"
        text_surface = self.font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        controls_text = "Управление: Стрелки ↑↓ - движение, ←→ - поворот, ESC - выход"
        controls_surface = self.font.render(controls_text, True, (255, 255, 255))
        self.screen.blit(controls_surface, (10, self.height - 30))

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()

            # Отрисовка
            if self.current_image:
                self.screen.blit(self.current_image, (0, 0))

            self.draw_info()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    simulator = CorridorSimulator()
    simulator.run()