import pygame

WIDTH, HEIGHT, TITLE = 1024, 800, "JeuBrawlstar"
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BG = pygame.transform.scale(pygame.image.load("assets/background-black.png"),(WIDTH, HEIGHT))

FPS = 20