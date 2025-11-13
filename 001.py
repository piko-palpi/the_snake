"""
Игра «Изгиб Питона» (Snake)
Описание:
Классическая змейка с проходом сквозь стены.
"""

import pygame
import random
import sys

# -------------------- Константы --------------------
CELL_SIZE = 20
FIELD_WIDTH = 640
FIELD_HEIGHT = 480
GRID_WIDTH = FIELD_WIDTH // CELL_SIZE
GRID_HEIGHT = FIELD_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FPS = 20


# -------------------- Базовый класс --------------------
class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self):
        """Инициализация позиции и цвета объекта."""
        self.position = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.body_color = None

    def draw(self, surface):
        """Метод для отрисовки объекта. Переопределяется в дочерних классах."""
        pass


# -------------------- Класс яблока --------------------
class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Создаёт яблоко в случайной позиции."""
        super().__init__()
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """
        Устанавливает случайное положение яблока на поле,
        избегая клеток, занятых змейкой.
        """
        while True:
            new_pos = (
                random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE,
            )
            if not snake_positions or new_pos not in snake_positions:
                self.position = new_pos
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


# -------------------- Класс змейки --------------------
class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Создаёт змейку в начальном состоянии."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)  # движение вправо
        self.next_direction = None
        self.body_color = GREEN

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.next_direction = new_direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        cur_x, cur_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (cur_x + dx) % FIELD_WIDTH   # проход через стены
        new_y = (cur_y + dy) % FIELD_HEIGHT
        new_head = (new_x, new_y)

        # Проверка столкновения с собой
        if new_head in self.positions[:-1]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(FIELD_WIDTH // 2, FIELD_HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None


# -------------------- Управление клавишами --------------------
def handle_keys(snake):
    """Обрабатывает нажатия клавиш и изменяет направление змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((CELL_SIZE, 0))


# -------------------- Основной игровой цикл --------------------
def main():
    """Главная функция игры. Запускает игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((FIELD_WIDTH, FIELD_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":
    main()
