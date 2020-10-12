import pygame

from pygame import *
from Fireball import Fireball
from Healthbar import Healthbar
from Entity import Entity

class Character(Entity):
    FIREBALL_COOLDOWN = 10

    def __init__(self, image, pos, platforms, health, *groups):
        super().__init__(image, pos, *groups)

        self.platforms = platforms
        self.health = health
        self.max_health = health

        self.fireballs = []
        self.fireball_img = None
        self.cool_down_counter = 0

        self.max_healthbar = None
        self.healthbar = None

    def draw_healthbar(self, *groups):  
        if self.healthbar != None:
            self.healthbar.kill()
            self.max_healthbar.kill()

        self.max_healthbar = Healthbar(self.max_health, "#FF0000", (self.rect.left, self.rect.bottom + 5),*groups)
        self.healthbar = Healthbar(self.health, "#00FF00", (self.rect.left, self.rect.bottom + 5),*groups)
    
    def shoot(self, targetX, targetY, *groups):
        
        if self.cool_down_counter == 0 :
            vectorX = targetX - self.rect.left
            vectorY = targetY - self.rect.top

            ball = Fireball((self.rect.left, self.rect.top), vectorX, vectorY, self.fireball_img, *groups)
            self.fireballs.append(ball)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.FIREBALL_COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    def move_fireballs(self, characters):
        self.cooldown()

        for fireball in self.fireballs:
            fireball.move()

            # collision with platform
            for p in self.platforms:
                if pygame.sprite.collide_rect(fireball, p):
                    fireball.kill()
                    if fireball in self.fireballs:
                        self.fireballs.remove(fireball)

            for character in characters:
                if pygame.sprite.collide_rect(fireball, character):
                    character.health -= 10
                    fireball.kill()
                    if fireball in self.fireballs:
                        self.fireballs.remove(fireball)

    def dispose(self):
        for fireball in self.fireballs:
            fireball.kill()
        self.fireballs.clear()

        self.healthbar.kill()
        self.max_healthbar.kill()
        self.kill()

    def collide(self, xvel, yvel):
        for p in self.platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left - 1 
                if xvel < 0:
                    self.rect.left = p.rect.right + 1
                if yvel > 0:
                    self.rect.bottom = p.rect.top - 1
                if yvel < 0:
                    self.rect.top = p.rect.bottom + 1

