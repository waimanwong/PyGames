import pygame
from math import sqrt

RED_FIREBALL = pygame.image.load("assets/fireball-red.png")
BLUE_FIREBALL = pygame.image.load("assets/fireball-blue.png")

class Fireball:
    def __init__(self, x, y, vx, vy, img):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 5

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        d = sqrt( (self.vx * self.vx) + (self.vy * self.vy ))
        ratio =  self.vel / d

        self.x += int(self.vx * ratio)
        self.y += int(self.vy * ratio)

    def off_screen(self, height):
        return not (0 <= self.y and self.y <= height)

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None