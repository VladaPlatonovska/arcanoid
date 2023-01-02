import math
import random
import pgzrun

from pgzero.actor import Actor
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

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


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
        self.position = Vector(self.x, self.y)

        self.ball = pygame.Rect(self.x, self.y, self.radius, self.speedX)



    def draw(self):
        pygame.draw.circle(surface, 'white', (self.x, self.y), self.radius)


    def paddle_collision(self):
        if paddle.x - self.radius <= self.x <= paddle.x + paddle.width and self.y >= paddle.y - self.radius:
            self.speedY *= random.choice([-1, 1])


    def update(self, dt):
        self.x -= self.speedX
        self.y -= self.speedY
        self.position = Vector(self.x, self.y)
        if self.x >= WIDTH or self.x <= 0:
            self.speedX *= -1
        if self.y >= HEIGHT or self.y <= 0:
            self.speedY *= -1


class Obstacle:
    def __init__(self, vector: Vector, color):
        self.x = vector.x
        self.y = vector.y
        self.position = vector
        self.radius = 15
        self.color = color
        self.o_dict = {}
        self.strength = 0

    def draw(self):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    # def touched_ball(self, b: Ball):
    #     distance = (b.position - self.position).magnitude()
    #     return distance < 20

    def get_strength(self):
        if self.y == 60:
            self.strength = 3
            self.color = 'red'
        elif self.y == 95:
            self.strength = 2
            self.color = 'orange'
        elif self.y == 130:
            self.strength = 1
            self.color = 'yellow'


ball = Ball()
obstacles = []
color_obstacles = ['yellow', 'orange', 'red']


class Hearts:
    def __init__(self, x, y):
        self.actor = Actor("heart", center=(x, y))


    def draw(self):
        self.actor.draw()

    def PlaceHeart(self, x, y):
        self.actor.width = x
        self.actor.height = y


hearts = []
for i in range(3):
    if i == 0:
        hearts.append(Hearts(15, 20))
    if i == 1:
        hearts.append(Hearts(45, 20))
    if i == 2:
        hearts.append(Hearts(75, 20))

def add_obstacles(color, obs, row):
    for obs_num in range(21):
        obs.append(Obstacle(row, color))
        row += Vector(40, 0)
    return set(obs)


def on_mouse_move(pos):
    paddle.where_to(pos)


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    for HEART in hearts:
        HEART.draw()
    for obstacle in obstacles:
        obstacle.draw()


def update(dt):
    paddle.update(dt)
    ball.update(dt)
    ball.paddle_collision()
    for obstacle in obstacles:
        distance = (ball.position - obstacle.position).magnitude()
        if distance < 25:
            if obstacle.strength != 1:
                obstacle.strength -= 1
                obstacle.color = color_obstacles[obstacle.strength - 1]
            else:
                obstacles.remove(obstacle)

            ball.speedY *= -1
            ball.speedX *= -1  # ????


row_vector = Vector(20, 60)
for colour in color_obstacles:
    add_obstacles(colour, obstacles, row_vector)
    row_vector += Vector(0, 35)

for obst in obstacles:
    obst.get_strength()


pgzrun.go()
