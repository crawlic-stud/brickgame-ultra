from functions import offset_sprite, draw_pixel_matrix
from sprites import EXPLOSION


class Animations:
    def __init__(self):
        self.anim_counter = 0
        self.frame_len = 3

        self.anim_explosion = len(EXPLOSION)
        self.explosion_x = 0
        self.explosion_y = 0

    def explosion(self, x, y):
        """Allows explosion to draw at certain location"""
        self.anim_explosion = 0

        # -2 offsets explosion's center to (x, y)
        self.explosion_x = x - 2
        self.explosion_y = y - 2

    def draw(self, screen):
        """Method that draws every animation if needed"""
        self.anim_counter += 1
        if self.anim_counter <= self.frame_len:

            # all animation draws go here
            if self.anim_explosion < len(EXPLOSION):
                for pos in offset_sprite(sprite=EXPLOSION[self.anim_explosion],
                                         offset_x=self.explosion_x,
                                         offset_y=self.explosion_y):
                    draw_pixel_matrix(screen, pos)

        else:
            self.anim_counter = 0
            self.anim_explosion += 1
