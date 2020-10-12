import pygame
import fireball
import constants

CHARACTER_SHELLY = pygame.image.load("assets/characters/shelly.png")
CHARACTER_FRANK = pygame.image.load("assets/characters/frank.png")

class Character:
    FIREBALL_COOLDOWN = 4

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.img = None
        self.velocity = 2
        self.fireballs = []
        self.fireball_img = None
        self.cool_down_counter = 0
        
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        self.draw_fireballs(window)
        self.draw_healthbar(window)

    def draw_fireballs(self, window):
        for fireball in self.fireballs:
            fireball.draw(window)

    def draw_healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.img.get_height() + 10, self.img.get_width() * (self.health/self.max_health), 10))

    def get_width(self):
        return self.img.get_width()
    
    def get_height(self):
        return self.img.get_height()

    def move_fireballs(self, objs):
        self.cooldown()

        destroyed_obj_count = 0

        for fireball in self.fireballs:
            fireball.move()

            if fireball.off_screen(constants.HEIGHT):
                self.fireballs.remove(fireball)
            else:
                for obj in objs:
                    if fireball.collision(obj):
                        obj.health -= 10
                        if fireball in self.fireballs:
                            self.fireballs.remove(fireball)

    def cooldown(self):
        if self.cool_down_counter >= self.FIREBALL_COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    def shoot(self, targetX, targetY):
        if self.cool_down_counter == 0 :
            vectorX = targetX - self.x
            vectorY = targetY - self.y

            ball = fireball.Fireball(self.x, self.y, vectorX, vectorY, self.fireball_img)
            self.fireballs.append(ball)
            self.cool_down_counter = 1

class MyCharacter(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.velocity = 10
        self.img = CHARACTER_SHELLY
        self.mask = pygame.mask.from_surface(self.img)
        self.fireball_img = fireball.RED_FIREBALL

class Enemy(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.img = CHARACTER_FRANK
        self.mask = pygame.mask.from_surface(self.img)
        self.fireball_img = fireball.BLUE_FIREBALL
    