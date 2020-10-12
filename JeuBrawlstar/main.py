import pygame
import random
import fireball
import character
import constants

# but du jeu:
# Gagner contre les adversaires
# DONE on contrôle un personnage
# DONE carte: rectangle
# adversaires
# le personnage peut attaquer les adversaires

pygame.font.init()

pygame.display.set_caption(constants.TITLE)


def main():
    gameIsRunning = True
    clock = pygame.time.Clock()

    lost_font = pygame.font.SysFont("comicsans", 60)
    lost = False
    lost_count = 0

    player = character.MyCharacter(int(constants.WIDTH / 2), int(constants.HEIGHT / 2))
    enemies = []

    # game rendering
    def redraw_window():
        # Draw background
        constants.WIN.blit(constants.BG, (0,0))

        # Draw enemies
        for enemy in enemies:
            enemy.draw(constants.WIN)

        # Draw player
        player.draw(constants.WIN)

        if lost:
            lost_label = lost_font.render("You lost!!", 1 , (255,255, 255))
            constants.WIN.blit(lost_label, (350, 350) )

        #Rendering
        pygame.display.update()

    def check_enemy_health():
        for enemy in enemies:
            if enemy.health <= 0 :
                enemies.remove(enemy)

    def move_player():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player.velocity > 0: 
            player.x -= player.velocity
        if keys[pygame.K_d] and player.x + player.velocity + player.get_width() < constants.WIDTH : 
            player.x += player.velocity
        if keys[pygame.K_w] and player.y + player.velocity > 0: 
            player.y -= player.velocity
        if keys[pygame.K_s] and player.y + player.velocity + player.get_height() + 10 < constants.HEIGHT: 
            player.y += player.velocity
    
    def player_shoot():
        mouse1, mouse2, mouse3 = pygame.mouse.get_pressed()
        if mouse1:
            targetX, targetY = pygame.mouse.get_pos()
            player.shoot(targetX, targetY)

    def move_enemies():
        for enemy in enemies:

            #move toward player
            if enemy.x < player.x:
                newEnemyX = enemy.x + enemy.velocity
            elif enemy.x > player.x:
                newEnemyX = enemy.x - enemy.velocity
            else:
                newEnemyX = enemy.x

            if enemy.y < player.y:
                newEnemyY = enemy.y + enemy.velocity
            elif enemy.y > player.y:
                newEnemyY = enemy.y - enemy.velocity
            else:
                newEnemyY = enemy.y

            if (0 < newEnemyX) and (newEnemyX + enemy.get_width() < constants.WIDTH):
                enemy.x = newEnemyX 

            if (0 < newEnemyY) and (newEnemyY + enemy.get_height() + 10 < constants.HEIGHT):
                enemy.y = newEnemyY 

    def enemies_shoot():
        for enemy in enemies:
            if random.randrange(0, 2 * constants.FPS) == 1:
                enemy.shoot(player.x, player.y)

    while gameIsRunning:
        clock.tick(constants.FPS)

        redraw_window()

        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > constants.FPS * 3:
                gameIsRunning = False
            else:
                continue

        if len(enemies) == 0:
            #spawn all enemies
            for i in range(5):
                enemyX = random.randrange(50, constants.WIDTH - 150)
                enemyY = random.randrange(50, constants.HEIGHT - 200)
                enemy = character.Enemy(enemyX, enemyY)
                enemies.append(enemy)

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsRunning = False
                print("Quit the game")

        move_player()
        player_shoot()

        check_enemy_health()

        move_enemies()
        enemies_shoot()

        player.move_fireballs(enemies)

        for enemy in enemies:
            enemy.move_fireballs( [ player ] )


main()