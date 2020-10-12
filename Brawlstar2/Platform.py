import pygame

from pygame import Color, Surface
from Constants import TILE_SIZE

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(Color("#DDDDDD"))
        self.rect = self.image.get_rect(topleft=pos)