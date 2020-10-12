import pygame
import random

from pygame import *
from Constants import *
from CameraAwareLayeredUpdates import *
from Player import *
from Platform import Platform
from Enemy import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                    PPPPPPPPPPP                          P",
        "P                    PPPPPPPPPPP                          P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                 PPPPPPPPPPPPPPPP                        P",
        "P                 PPPPPPPPPPPPPPPP                        P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P", 
        "P                                                         P",
        "P                                                         P",
        "P                                           PP            P",
        "P                                           PP            P",
        "P                                           PP            P",
        "P                                           PP            P",
        "P                 PPPPPPPPPPP               PP            P",
        "P                 PPPPPPPPPPP               PP            P",
        "P                 PPPPPPPPPPP                             P",
        "P                 PPPPPPPPPPP                             P",
        "P                 PPPPPPPPPPP                             P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "P                                                         P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]


    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE), 100)
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    # build the level
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                Platform((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    enemies = []

    lost = False
    lost_count = 0
    lost_font = pygame.font.SysFont("comicsans", 60)
    
    while 1:

        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                return
            else:
                print("You lost !!!")
                continue

        if len(enemies) == 0:
            #spawn all enemies
            for i in range(5):
                enemyX = random.randrange(50, level_width - 150)
                enemyY = random.randrange(50, level_height - 200)
                enemy = Enemy(platforms, (enemyX, enemyY), 100, entities)
                enemies.append(enemy)

        # handle events
        for e in pygame.event.get():
            if e.type == QUIT: 
                return
            
        mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
        if mouse1:
            mouseX, mouseY = pygame.mouse.get_pos()

            targetX = mouseX - SCREEN_CENTER_X + player.rect.left
            targetY = mouseY - SCREEN_CENTER_Y + player.rect.top
            
            player.shoot(targetX, targetY, entities)

        player.draw_healthbar(entities)
        player.move_fireballs(enemies)

        for enemy in enemies:
            if enemy.health <= 0 :
                enemy.dispose()
                enemies.remove(enemy)
            else:
                enemy.move(player)
                enemy.draw_healthbar(entities)
                if random.randrange(0, 2 * FPS) == 1:
                    enemy.shoot(player.rect.left, player.rect.top, entities)
                enemy.move_fireballs([player])


        entities.update()
        screen.fill((0, 0, 0))
        entities.draw(screen)
        pygame.display.update()

        timer.tick(FPS)


if __name__ == "__main__":
    main()