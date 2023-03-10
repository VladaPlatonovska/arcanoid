import math
import random
import pgzrun
import time
from pgzero.actor import Actor
import pygame
from vector import Vector

WIDTH = 600
HEIGHT = 400
surface = pygame.display.set_mode((WIDTH, HEIGHT))


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
        pygame.draw.rect(surface, 'cadetblue3', self.rectangle)

    def update(self, dt):
        # moving the paddle
        self.x = self.goal.x - self.width / 2  # so that the cursor is in the middle
        # checking if paddle is not 'outside' the screen
        if self.goal.x < self.width / 2:  # < 60
            self.x = 0
        if self.goal.x > WIDTH - self.width / 2:  # > 540
            self.x = WIDTH - self.width  # = 480
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)


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
        pygame.draw.circle(surface, 'lavenderblush2', (self.x, self.y), self.radius)

    def paddle_collision(self):
        # checking the ball touches the paddle by x and y
        if paddle.x - self.radius <= self.x <= paddle.x + paddle.width and self.y >= paddle.y - self.radius:
            # change the direction of the ball
            self.speedY *= -1

    def update(self, dt):
        self.x -= self.speedX
        self.y -= self.speedY
        self.position = Vector(self.x, self.y)
        # check if the ball touches left or right side
        if self.x >= WIDTH - self.radius or self.x <= self.radius:
            # change the direction of the ball
            self.speedX *= -1
        # check if the ball touches the upper wall
        if self.y >= HEIGHT or self.y <= 0:
            # change the direction of the ball
            self.speedY *= -1

    def check_ball_fall(self, dt):
        #check if the ball fall down
        if ball.y == 390:
            hearts.pop()
            self.speedY *= -1
            self.x = int(WIDTH / 2 - self.radius / 2)
            self.y = int(HEIGHT - self.radius * 4)
            self.x -= self.speedX
            self.y -= self.speedY
            self.position = Vector(self.x, self.y)
            # delay the time of renewing the game
            time.sleep(1)


class RectObstacle:
    def __init__(self, vector: Vector, color):
        self.x = vector.x
        self.y = vector.y
        self.color = color
        self.width = 50
        self.height = 15
        self.strength = 0
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(surface, self.color, self.rectangle)

    def get_strength(self):
        # giving each rectangle a strength according to its position
        if self.y == 45:
            self.strength = 3
            self.color = color_obstacles[2]

        elif self.y == 170:
            self.strength = 1
            self.color = color_obstacles[0]

    def rect_obst_collision(self, b: Ball):
        # checking if ball hits the obstacle
        if self.x - b.radius <= b.x <= self.x + self.width and b.y <= self.y + self.height + b.radius:
            return True


class CircleObstacle:
    def __init__(self, vector: Vector, color):
        self.x = vector.x
        self.y = vector.y
        self.position = vector
        self.radius = 15
        self.color = color
        self.strength = 0

    def draw(self):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_strength(self):
        # giving each obstacle a strength according to its positions
        if self.y == 80:
            self.strength = 3
            self.color = color_obstacles[2]
        elif self.y == 115:
            self.strength = 2
            self.color = color_obstacles[1]
        elif self.y == 150:
            self.strength = 1
            self.color = color_obstacles[0]


class Hearts:
    def __init__(self, x, y):
        self.actor = Actor("heart", center=(x, y))

    def draw(self):
        self.actor.draw()

    def place_heart(self, x, y):
        self.actor.width = x
        self.actor.height = y


class BonusHearts:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.actor = Actor("heart", center=(x, y))
        self.actor.width = 30
        self.actor.height = 29

    def move(self):
        # moving the bonus down
        self.y += 2
        self.actor = Actor("heart", center=(self.x, self.y))

    def draw(self):
        self.actor.draw()

    def touches_paddle(self, p: Paddle):
        # checking if player catches the bonus
        if p.x - self.actor.width <= self.x <= p.x + p.width + self.actor.width and self.y >= p.y - self.actor.height:
            return True


class BonusLength:
    def __init__(self, pos: Vector):
        self.position = pos
        self.start_time = None
        self.velocity = Vector(0, 2)
        self.radius = 10

    def move(self):
        # moving the bonus downwards
        self.position += self.velocity

    def draw(self):
        screen.draw.filled_circle((self.position.x, self.position.y), self.radius, "gold2")

    def touches_paddle(self, p: Paddle):
        # checking if player catches the bonus
        if p.x - self.radius <= self.position.x <= p.x + p.width + self.radius and self.position.y > p.y - self.radius:
            return True


def add_obstacles(color, obs, row):
    # creating rows of round obstacles
    for obs_num in range(15):
        obs.append(CircleObstacle(row, color))
        row += Vector(40, 0)
    return set(obs)


def add_rect_obstacles(color, obs, row):
    # creating rows of rectangular obstacles
    for obs_num in range(10):
        obs.append(RectObstacle(row, color))
        row += Vector(60, 0)
    return set(obs)


def on_mouse_move(pos):
    # getting the position of the mouse
    paddle.where_to(pos)


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    for HEART in hearts:
        HEART.draw()
    for obstacle in circle_obstacles:
        obstacle.draw()
    for obstacle in rect_obstacles:
        obstacle.draw()
    for bonus in bonus_hearts:
        bonus.draw()
    for bonus in length_bonuses:
        bonus.draw()


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
    if len(circle_obstacles) == 0 and len(rect_obstacles) == 0 and len(hearts) != 0:
        message_display("You Win!")
        quit()
    if len(hearts) == 0:
        message_display("You Lose!")
        quit()


active_length_bonuses = []
length_bonuses = []
white = (255, 255, 255)
bonus_hearts = []
ball = Ball()
circle_obstacles = []
rect_obstacles = []
color_obstacles = ['yellow1', 'orange', 'red2']
color_rect = ['red2', 'yellow1']
paddle = Paddle()

hearts = []

for i in range(3):
    if i == 0:
        hearts.append(Hearts(15, 20))
    if i == 1:
        hearts.append(Hearts(45, 20))
    if i == 2:
        hearts.append(Hearts(75, 20))


def update(dt):
    paddle.update(dt)
    ball.update(dt)
    ball.paddle_collision()
    ball.check_ball_fall(dt)
    check_win()
    for obstacle in circle_obstacles:
        # checking if ball touches the round obstacle
        distance = (ball.position - obstacle.position).magnitude()
        if distance < 25:
            if obstacle.strength != 1:
                # making obstacles 'weaker' and changing their color according to strength
                obstacle.strength -= 1
                obstacle.color = color_obstacles[obstacle.strength - 1]
            else:
                circle_obstacles.remove(obstacle)

            # changing the y-direction of the ball
            ball.speedY *= -1

    for rect in rect_obstacles:
        if rect.rect_obst_collision(ball):
            if rect.strength != 1:
                rect.strength -= 1
                rect.color = color_obstacles[rect.strength - 1]
            else:
                rect_obstacles.remove(rect)

            ball.speedY *= -1

    # randomly generating bonuses
    if random.random() < 0.0005:
        bonus_hearts.append(BonusHearts(random.randint(0, WIDTH), -30))
        length_bonuses.append(BonusLength(Vector(random.randint(0, WIDTH), -10)))

    # actions for heart bonuses
    for bonus in bonus_hearts:
        bonus.move()
        if bonus.touches_paddle(paddle):
            bonus_hearts.remove(bonus)
            if len(hearts) == 1:
                hearts.append(Hearts(45, 20))

            elif len(hearts) == 2:
                hearts.append(Hearts(75, 20))

        elif bonus.y > HEIGHT:
            bonus_hearts.remove(bonus)

    # actions for length bonuses
    for bonus_l in length_bonuses:
        bonus_l.move()
        if bonus_l.touches_paddle(paddle):
            length_bonuses.remove(bonus_l)
            bonus_l.start_time = time.time()
            active_length_bonuses.append(bonus_l)

            paddle.width *= 1.5
        elif bonus_l.position.y > HEIGHT:
            length_bonuses.remove(bonus_l)

    for bonus_l in active_length_bonuses:
        if time.time() - bonus_l.start_time > 5:
            active_length_bonuses.remove(bonus_l)
            paddle.width /= 1.5


# creating obstacles and assigning them their strengths
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
