import pgzrun
import pygame

WIDTH = 600
HEIGHT = 400
surface = pygame.display.set_mode((WIDTH, HEIGHT))


class Paddle:
    def __init__(self):
        self.height = 15
        self.width = 120
        self.x = int(WIDTH/2 - self.width/2)
        # the rectangle x position is the top left point of the rectangle
        self.y = int(HEIGHT - self.height * 2)  # so it isn't at the very bottom
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(surface, 'cyan', self.rectangle)


paddle = Paddle()


def draw():
    paddle.draw()


def update(dt):
    pass


pgzrun.go()
