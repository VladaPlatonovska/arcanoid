import math
import random
import pgzrun
import time
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
        self.x = int(WIDTH / 2 - self.width / 2)
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
            self.speedY *= -1

    def update(self, dt):
        self.x -= self.speedX
        self.y -= self.speedY
        self.position = Vector(self.x, self.y)
        if self.x >= WIDTH or self.x <= 0:
            self.speedX *= -1
        if self.y >= HEIGHT or self.y <= 0:
            self.speedY *= -1

    def check_ball_fall(self, dt):
        if ball.y == 390:
            hearts.pop()
            self.speedY *= -1
            self.x = int(WIDTH / 2 - self.radius / 2)
            self.y = int(HEIGHT - self.radius * 4)
            self.x -= self.speedX
            self.y -= self.speedY
            self.position = Vector(self.x, self.y)
            time.sleep(1)


class RectObstacle:
    def __init__(self, vector: Vector, color):
        self.x = vector.x
        self.y = vector.y
        self.position = vector
        self.color = color
        self.width = 50
        self.height = 15
        self.strength = 0
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(surface, self.color, self.rectangle)

    def get_strength(self):
        if self.y == 45:
            self.strength = 3
            self.color = color_obstacles[2]
        # elif self.y == 115:
        #     self.strength = 2
        #     self.color = color_obstacles[1]
        elif self.y == 170:
            self.strength = 1
            self.color = color_obstacles[0]

    def rect_obst_collision(self, b: Ball):
        if self.x - b.radius <= b.x <= self.x + self.width and b.y <= self.y + self.height + b.radius:
            return True


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
        if self.y == 80:
            self.strength = 3
            self.color = color_obstacles[2]
        elif self.y == 115:
            self.strength = 2
            self.color = color_obstacles[1]
        elif self.y == 150:
            self.strength = 1
            self.color = color_obstacles[0]


ball = Ball()
circle_obstacles = []
rect_obstacles = []
color_obstacles = ['yellow', 'orange', 'red']
color_rect = ['red', 'yellow']


class Hearts:
    def __init__(self, x, y):
        self.actor = Actor("heart", center=(x, y))

    def draw(self):
        self.actor.draw()

    def place_heart(self, x, y):
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


def add_rect_obstacles(color, obs, row):
    for obs_num in range(15):
        obs.append(RectObstacle(row, color))
        row += Vector(60, 0)
    return set(obs)

def on_mouse_move(pos):
    paddle.where_to(pos)


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    # rect_o.draw()
    for HEART in hearts:
        HEART.draw()
    for obstacle in circle_obstacles:
        obstacle.draw()
    for obst in rect_obstacles:
        obst.draw()


white = (255, 255, 255)


def text_objects(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((WIDTH / 2), (HEIGHT / 2))
    surface.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)


def check_win():
    if len(circle_obstacles) == 0 and len(hearts) != 0:
        message_display("You Win!")
        quit()
    if len(hearts) == 0:
        # font2 = pygame.font.SysFont('didot.ttc', 72)
        # img2 = font2.render('You Lose', True, white)
        # surface.blit(img2, (200, 200))
        # pygame.display.update()
        # time.sleep(2)
        message_display("You Lose!")
        quit()


def update(dt):
    paddle.update(dt)
    ball.update(dt)
    ball.paddle_collision()
    ball.check_ball_fall(dt)
    check_win()
    for obstacle in circle_obstacles:
        distance = (ball.position - obstacle.position).magnitude()
        if distance < 25:
            if obstacle.strength != 1:
                obstacle.strength -= 1
                obstacle.color = color_obstacles[obstacle.strength - 1]
            else:
                circle_obstacles.remove(obstacle)

            ball.speedY *= -1

    for rect in rect_obstacles:
        if rect.rect_obst_collision(ball):
            if rect.strength != 1:
                rect.strength -= 1
                rect.color = color_obstacles[rect.strength - 1]
            else:
                rect_obstacles.remove(rect)

            ball.speedY *= -1


row_circle = Vector(20, 80)
for colour in color_obstacles:
    add_obstacles(colour, circle_obstacles, row_circle)
    row_circle += Vector(0, 35)

for obst in circle_obstacles:
    obst.get_strength()

row_rect = Vector(5, 45)
for colour in color_rect:
    add_rect_obstacles(colour, rect_obstacles, row_rect)
    row_rect += Vector(0, 125)

for rect_o in rect_obstacles:
    rect_o.get_strength()

pgzrun.go()
