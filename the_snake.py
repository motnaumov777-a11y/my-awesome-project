from random import randint

import pygame

pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
OUTLINE_COLOR = (93, 216, 228)

# Скорость движения змейки
SPEED = 8

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Исправлено: кортеж вместо списка
        self.body_color = None

    @staticmethod
    def draw_rect(position, body_color):
        rect = pygame.Rect((position[0], position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, OUTLINE_COLOR, rect, 1)

    def draw(self):
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}.'
        )


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):  # Убрал staticmethod
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,  # Исправлено: GRID_WIDTH - 1 вместо GRID_WIDTH - GRID_SIZE
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.reset()

    def update_direction(self, next_direction):
        if next_direction:
            self.direction = next_direction

    def move(self):
        head_position = self.get_head_position()
        x_point = head_position[0]
        y_point = head_position[1]

        # Обработка выхода за границы экрана
        if x_point >= SCREEN_WIDTH:
            x_point = 0
        elif x_point < 0:
            x_point = SCREEN_WIDTH - GRID_SIZE

        if y_point >= SCREEN_HEIGHT:
            y_point = 0
        elif y_point < 0:
            y_point = SCREEN_HEIGHT - GRID_SIZE

        # Расчет новой позиции головы
        new_x = x_point + self.direction[0] * GRID_SIZE
        new_y = y_point + self.direction[1] * GRID_SIZE
        
        # Обновление позиций
        self.positions.insert(0, (new_x, new_y))
        self.last = self.positions.pop()

    def draw(self):
        for position in self.positions[:-1]:
            self.draw_rect(position, self.body_color)

        # Отрисовка головы змейки
        head = self.get_head_position()
        self.draw_rect(head, self.body_color)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_body_positions(self):  # Переименовал для ясности
        return self.positions[1:]


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    apple = Apple()
    snake = Snake()
    
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()
        
        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        
        # Отрисовка объектов
        apple.draw()
        snake.draw()
        
        # Проверка столкновений
        if snake.get_head_position() == apple.position:
            # Увеличение змейки
            snake.positions.append(snake.last)
            apple = Apple()
        
        # Проверка столкновения с собой
        if snake.get_head_position() in snake.get_body_positions():
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple = Apple()
        
        pygame.display.update()


if __name__ == '__main__':
    main()