import pygame
import sys
import math
import time
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Simulator")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRASS = (40, 180, 40)
ROAD = (60, 60, 60)
CHECKPOINT_COLORS = {
    'active': (0, 255, 0),
    'inactive': (255, 255, 0),
    'passed': (0, 150, 255)
}

# Настройки игры
clock = pygame.time.Clock()
FPS = 60


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 70
        self.speed = 0
        self.max_speed = 8
        self.acceleration = 0.2
        self.rotation = 0
        self.rotation_speed = 3

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, BLUE, (5, 5, self.width - 10, 15))  # Переднее стекло
        pygame.draw.rect(self.image, BLUE, (5, self.height - 20, self.width - 10, 15))  # Заднее стекло
        pygame.draw.rect(self.image, YELLOW, (2, 2, 6, 6))  # Левая фара
        pygame.draw.rect(self.image, YELLOW, (self.width - 8, 2, 6, 6))  # Правая фара
        pygame.draw.rect(self.image, RED, (2, self.height - 8, 6, 6))  # Левый фонарь
        pygame.draw.rect(self.image, RED, (self.width - 8, self.height - 8, 6, 6))  # Правый фонарь
        pygame.draw.rect(self.image, WHITE, (10, 20, self.width - 20, 5))
        pygame.draw.rect(self.image, WHITE, (10, 40, self.width - 20, 5))

        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        rad = math.radians(self.rotation)
        self.x += self.speed * math.sin(rad)
        self.y -= self.speed * math.cos(rad)

        self.image = pygame.transform.rotate(self.original_image, -self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class Track:
    def __init__(self):
        self.checkpoints = []
        self.next_checkpoint = 0
        self.laps = 0
        self.max_laps = 1
        self.track_mask = None
        self.track_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.generate_circular_track()

    def generate_circular_track(self):
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        radius_outer = 250
        radius_inner = 130
        angle_step = 15

        points_outer = []
        points_inner = []

        for angle in range(0, 360, angle_step):
            rad = math.radians(angle)
            outer_x = center_x + math.cos(rad) * radius_outer
            outer_y = center_y + math.sin(rad) * radius_outer
            inner_x = center_x + math.cos(rad) * radius_inner
            inner_y = center_y + math.sin(rad) * radius_inner
            points_outer.append((outer_x, outer_y))
            points_inner.insert(0, (inner_x, inner_y))

        pygame.draw.polygon(self.track_surface, ROAD, points_outer)
        pygame.draw.polygon(self.track_surface, GRASS, points_inner)

        self.track_mask = pygame.mask.from_surface(self.track_surface)

        cp_angles = [0, 90, 180, 270]
        for angle in cp_angles:
            rad = math.radians(angle)
            cx = center_x + math.cos(rad) * (radius_inner + 60)
            cy = center_y + math.sin(rad) * (radius_inner + 60)
            cp_rect = pygame.Rect(cx - 20, cy - 40, 40, 80)
            self.checkpoints.append({
                'rect': cp_rect,
                'passed': False,
                'next': False
            })

        self.checkpoints[0]['next'] = True

    def draw(self, surface):
        surface.fill(GRASS)
        surface.blit(self.track_surface, (0, 0))

        for cp in self.checkpoints:
            color = CHECKPOINT_COLORS['active'] if cp['next'] else CHECKPOINT_COLORS['passed'] if cp['passed'] else \
            CHECKPOINT_COLORS['inactive']
            pygame.draw.rect(surface, color, cp['rect'], 3)

    def check_collision(self, car):
        offset_x = int(car.x - car.width // 2)
        offset_y = int(car.y - car.height // 2)
        return self.track_mask.overlap(car.mask, (offset_x, offset_y)) is None

    def check_checkpoint(self, car):
        cp = self.checkpoints[self.next_checkpoint]
        if car.rect.colliderect(cp['rect']):
            cp['passed'] = True
            cp['next'] = False
            self.next_checkpoint = (self.next_checkpoint + 1) % len(self.checkpoints)
            self.checkpoints[self.next_checkpoint]['next'] = True
            if self.next_checkpoint == 0:
                self.laps += 1
                return True
        return False


def main():
    car = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130)
    track = Track()
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 24)
    start_time = time.time()
    current_time = 0
    best_time = float('inf')
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return main()

        keys = pygame.key.get_pressed()

        if not game_over and track.laps < track.max_laps:
            current_time = time.time() - start_time
            if keys[pygame.K_UP]:
                car.speed = min(car.speed + car.acceleration, car.max_speed)
            elif keys[pygame.K_DOWN]:
                car.speed = max(car.speed - car.acceleration, -car.max_speed / 2)
            else:
                car.speed *= 0.98

            if abs(car.speed) > 1:
                if keys[pygame.K_LEFT]:
                    car.rotation += car.rotation_speed
                if keys[pygame.K_RIGHT]:
                    car.rotation -= car.rotation_speed

            car.update()

            if track.check_collision(car):
                car.speed *= -0.4
                car.rotation += 10

            if track.check_checkpoint(car):
                if track.next_checkpoint == 0 and current_time < best_time:
                    best_time = current_time

            if track.laps >= track.max_laps:
                game_over = True

        track.draw(screen)
        car.draw(screen)

        time_text = font.render(f"Time: {current_time:.1f}s", True, WHITE)
        screen.blit(time_text, (20, 20))

        speed_text = font.render(f"Speed: {abs(car.speed):.1f}", True, WHITE)
        screen.blit(speed_text, (20, 60))

        next_cp_text = small_font.render(f"Next CP: {track.next_checkpoint + 1}/{len(track.checkpoints)}", True, WHITE)
        screen.blit(next_cp_text, (20, 100))

        if best_time != float('inf'):
            best_text = font.render(f"Best Time: {best_time:.1f}s", True, WHITE)
            screen.blit(best_text, (SCREEN_WIDTH - 300, 20))

        if game_over:
            finish_text = font.render("Race Finished! Press R to Restart", True, CHECKPOINT_COLORS['active'])
            screen.blit(finish_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()