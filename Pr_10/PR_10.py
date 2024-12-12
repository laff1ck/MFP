import pygame
import random
import math

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Круговая гонка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Параметры круга
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200
FINISH_LINE_RADIUS = 10
FINISH_ANGLE = 0  # Угол финишной точки

# Параметры гонки
NUM_PARTICIPANTS = 4
NUM_LAPS = 4
FPS = 60
FORWARD_ONLY_FRAMES = 8 * FPS

# Генерация участников
participants = []
winners = []
colors = [RED, GREEN, BLUE, YELLOW]

for i in range(NUM_PARTICIPANTS):
    participant = {
        "angle": math.pi,                    # Угол начальной позиции (все стартуют на противоположной стороне круга)
        "speed": random.uniform(0.02, 0.05),   # Скорость
        "direction": 1,                        # Направление (1: вперед)
        "laps": 0,                             # Пройденные круги
        "color": colors[i],                    # Цвет участника
        "reverse_time": 0,                     # Оставшееся время движения назад
        "last_reverse": -5 * FPS,              # Последний момент смены направления
        "crossed_finish": False                # Флаг пересечения финишной линии
    }
    participants.append(participant)

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Функция обновления положения участника
def update_position(participant, frame):
    if frame > FORWARD_ONLY_FRAMES:  # Проверяем, прошло ли время движения только вперед
        if participant["reverse_time"] > 0:
            participant["reverse_time"] -= 1
            participant["direction"] = -1
        else:
            participant["direction"] = 1

        # Случайное изменение направления
        if frame - participant["last_reverse"] >= 5 * FPS and random.random() < 0.02:
            participant["reverse_time"] = FPS  # 1 секунда назад
            participant["last_reverse"] = frame

    participant["angle"] += participant["speed"] * participant["direction"]

    # Проверка пересечения финишной линии (угол 0)
    current_angle = participant["angle"] % (2 * math.pi)
    if participant["direction"] == 1 and not participant["crossed_finish"] and FINISH_ANGLE - 0.1 <= current_angle <= FINISH_ANGLE + 0.1:
        participant["laps"] += 1
        participant["crossed_finish"] = True
    elif current_angle > FINISH_ANGLE + 0.1 or current_angle < FINISH_ANGLE - 0.1:
        participant["crossed_finish"] = False

    # Нормализация угла
    if participant["angle"] >= 2 * math.pi:
        participant["angle"] -= 2 * math.pi
    elif participant["angle"] < 0:
        participant["angle"] += 2 * math.pi

# Функция отображения участников
def draw_participants():
    for participant in participants:
        x = CENTER[0] + RADIUS * math.cos(participant["angle"])
        y = CENTER[1] + RADIUS * math.sin(participant["angle"])
        pygame.draw.circle(screen, participant["color"], (int(x), int(y)), 10)

# Функция отображения таблицы лидеров
def draw_leaderboard():
    leaderboard = sorted(participants, key=lambda p: (-p["laps"], -p["angle"]))
    for idx, participant in enumerate(leaderboard):
        text = font.render(f"{idx + 1}. Круги: {participant['laps']}", True, participant["color"])
        screen.blit(text, (10, 50 + idx * 30))


# Функция отображения списка победителей
def draw_winners():
    for idx, participant in enumerate(winners):
        text = font.render(f"{idx + 1}. Победитель: Круги: {participant['laps']}", True, participant["color"])
        screen.blit(text, (10, 300 + idx * 30))


# Функция отображения финишной точки
def draw_finish_line():
    x = CENTER[0] + RADIUS * math.cos(FINISH_ANGLE)
    y = CENTER[1] + RADIUS * math.sin(FINISH_ANGLE)
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), FINISH_LINE_RADIUS)

# Главный цикл игры
clock = pygame.time.Clock()
running = True
frame = 0

while running:
    screen.fill(WHITE)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление состояния участников
    for participant in participants:
        if participant["laps"] < NUM_LAPS:
            update_position(participant, frame)
        elif participant not in winners:
            winners.append(participant)

    # Отображение круга
    pygame.draw.circle(screen, BLACK, CENTER, RADIUS, 2)

    # Отображение финишной точки
    draw_finish_line()

    # Отображение участников
    draw_participants()

    # Отображение таблицы лидеров
    draw_leaderboard()

    # Отображение списка победителей
    draw_winners()

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)
    frame += 1

# Завершение pygame
pygame.quit()
