import pygame

from pygame import *
from Character import Character
from Fireball import BLUE_FIREBALL
from Healthbar import Healthbar

CHARACTER_FRANK = pygame.image.load("assets/characters/frank.png")

class Enemy(Character):
    def __init__(self, platforms, pos, health, *groups):
        super().__init__(CHARACTER_FRANK, pos, platforms, health, *groups)
        self.speed = 2
        self.fireball_img = BLUE_FIREBALL
    
    def move(self, targetRect):
        targetX, targetY = targetRect.rect.left, targetRect.rect.top

        #move toward player
        if self.rect.left < targetX:
            self.rect.left +=  self.speed
            self.collide(self.speed, 0)

        elif self.rect.left > targetX:
            self.rect.left -= self.speed
            self.collide(-self.speed, 0)
        
        if self.rect.top < targetY:
            self.rect.top += self.speed
            self.collide(0, self.speed)

        elif self.rect.top > targetY:
            self.rect.top -= self.speed
            self.collide(0, -self.speed)
       

