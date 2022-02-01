from src.__init__ import *


class Entity:
    def __init__(self, pos, sprite):
        self.x, self.y = pos
        self.sprite = offset_sprite(sprite, *pos)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.sprite = offset_sprite(self.sprite, dx, dy)

    def get_pos(self):
        return get_shape_pos(self.sprite)

    def draw(self, screen):
        for pixel in self.sprite:
            draw_pixel_matrix(screen, pixel)


