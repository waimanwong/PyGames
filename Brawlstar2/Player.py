import pygame

from pygame import *
from Character import Character
from Fireball import RED_FIREBALL

CHARACTER_SHELLY = pygame.image.load("assets/characters/shelly.png")

class Player(Character):
    def __init__(self, platforms, pos, health):
        super().__init__(CHARACTER_SHELLY, pos, platforms, health)
        self.speed = 4
        self.fireball_img = RED_FIREBALL
        
    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            self.rect.top -= self.speed
            self.collide(0, -self.speed)
        if pressed[K_s]:
            self.rect.top += self.speed
            self.collide(0, self.speed)
        if pressed[K_a]:
            self.rect.left -= self.speed
            self.collide(-self.speed, 0)
        if pressed[K_d]:
            self.rect.left += self.speed
            self.collide(self.speed, 0)
