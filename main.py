import random
import pgzrun
import pygame

WIDTH = 600
HEIGHT = 400
surface = pygame.display.set_mode((WIDTH, HEIGHT))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Paddle:
    def __init__(self):
        self.goal = Vector(0, 0)
        self.height = 15
        self.width = 120
        self.x = int(WIDTH/2 - self.width/2)
        # the rectangle x position is the top left point of the rectangle
        self.y = int(HEIGHT - self.height * 2)  # so it isn't at the very bottom
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def where_to(self, pos):
        # getting the coordinates of the mouse
        self.goal = Vector(pos[0], self.y)

    def draw(self):
        pygame.draw.rect(surface, 'cyan', self.rectangle)

    def update(self, dt):
        # moving the paddle
        self.x = self.goal.x - self.width / 2  # so that the cursor is in the middle
        # checking if paddle is not 'outside' the screen
        if self.goal.x < self.width / 2:  # < 60
            self.x = 0
        if self.goal.x > WIDTH - self.width / 2:  # > 540
            self.x = WIDTH - self.width  # = 480
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)


paddle = Paddle()


class Ball:

    def __init__(self):
        self.goal = Vector(0, 0)
        self.radius = 10
        self.x = int(WIDTH / 2 - self.radius / 2)
        self.y = int(HEIGHT - self.radius * 4)
        self.speedX = 3
        self.speedY = 3

        # ball_rect = int(self.radius * 2 ** 0.5)
        # self.ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
        # self.x, self.y = 300, 350
        self.ball = pygame.Rect(self.x, self.y, self.radius, self.speedX)



    def draw(self):
        pygame.draw.circle(surface, 'white', (self.x, self.y), self.radius)

    # pygame.draw.circle(screen, (255, 255, 0), (random_x, falling_y), random_size)
    def paddle_left_collision(self):
        if paddle.x - paddle.width <= self.x <= paddle.x + paddle.width and paddle.y <= self.y <= paddle.y + paddle.height:
            # self.speedX *= random.choice([-1, 1])
            self.speedY *= random.choice([-1, 1])


    def update(self, dt):
        self.x -= self.speedX
        self.y -= self.speedY
        if self.x >= WIDTH or self.x <= 0:
            self.speedX *= -1
        if self.y >= HEIGHT or self.y <= 0:
            self.speedY *= -1


ball = Ball()



def on_mouse_move(pos):
    paddle.where_to(pos)
    ball.paddle_left_collision()


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()


def update(dt):
    paddle.update(dt)
    ball.update(dt)


pgzrun.go()
