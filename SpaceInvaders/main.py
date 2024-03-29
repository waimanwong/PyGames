import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT, TITLE = 1024, 800, "Ma PS4 à moi"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Load images
RED_SPACE_SHIP =    pygame.image.load("assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP =  pygame.image.load("assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP =   pygame.image.load("assets/pixel_ship_blue_small.png")

#Player player
YELLOW_SPACE_SHIP = pygame.image.load("assets/pixel_ship_yellow.png")

# Lasers
RED_LASER =     pygame.image.load("assets/pixel_laser_red.png")
GREEN_LASER =   pygame.image.load("assets/pixel_laser_green.png")
BLUE_LASER =    pygame.image.load("assets/pixel_laser_blue.png")
YELLOW_LASER =  pygame.image.load("assets/pixel_laser_yellow.png")

#Background
BG = pygame.transform.scale(pygame.image.load("assets/background-black.png"),(WIDTH, HEIGHT))

#Game settings
FPS = 60

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (0 <= self.y and self.y <= height)

    def collision(self, obj):
        return collide(obj, self)

class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0 :
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()

        destroyed_obj_count = 0

        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        destroyed_obj_count += 1
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

        return destroyed_obj_count

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0 :
            laser = Laser(self.x - 10, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    gameIsRunning = True
    clock = pygame.time.Clock()

    level = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    player_vel = 7
    player = Player(300, 620)
    laser_vel = 4
    enemies = []
    wave_length = 5
    enemy_vel = 1
    score = 0
    lost = False
    lost_count = 0

    def redraw_window():
        # Draw background
        WIN.blit(BG, (0,0))

        # Draw text
        health_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(health_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
                
        # Draw enemies
        for enemy in enemies:
            enemy.draw(WIN)

        # Draw player
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!!", 1 , (255,255, 255))
            WIN.blit(lost_label, (350, 350) )

        pygame.display.update()

    while gameIsRunning:
        clock.tick(FPS)

        redraw_window()
        
        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                gameIsRunning = False
            else:
                continue

        if len(enemies) == 0:
            #new level
            level += 1
            wave_length += 5

            #spawn all enemies
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, WIDTH-100),
                    random.randrange(-1500, -100),
                    random.choice(["red", "blue", "green"])
                )
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsRunning = False
                print("Quit the game")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0: 
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH : 
            player.x += player_vel
        if keys[pygame.K_w] and player.y + player_vel > 0: 
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 10 < HEIGHT: 
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -=10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT :
                 # enemy hits the base
                enemies.remove(enemy)
            
        score += player.move_lasers(-laser_vel, enemies)

def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicsans", 70)
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width() / 2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()