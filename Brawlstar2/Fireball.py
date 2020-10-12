import pygame
from math import sqrt

RED_FIREBALL = pygame.image.load("assets/fireball-red.png")
BLUE_FIREBALL = pygame.image.load("assets/fireball-blue.png")

class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy, img, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.vx = vx
        self.vy = vy
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = 5

    def move(self):
        if self.vx == 0 and self.vy == 0:
            return

        d = sqrt( (self.vx * self.vx) + (self.vy * self.vy ))
        ratio =  self.vel / d

        self.rect.left += int(self.vx * ratio)
        self.rect.top += int(self.vy * ratio)

    