from Entity import Entity
from pygame import Surface, Color

class Healthbar(Entity):
    def __init__(self, health, color, pos, *groups):

        self.image = Surface((health, 10))
        self.image.fill(Color(color))

        super().__init__(self.image, pos, *groups)




        