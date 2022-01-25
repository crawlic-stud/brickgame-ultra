from functions import offset_sprite, draw_pixel_matrix
from sprites import EXPLOSION, CURTAIN


class Animations:
    def __init__(self):
        self.anim_counter = 0
        self.frame_len = 3

        self.anim_explosion = len(EXPLOSION) - 1
        self.explosion_x = 0
        self.explosion_y = 0

        self.anim_loading = len(CURTAIN) - 1

    def explosion(self, x, y):
        """Allows explosion to draw at certain location"""
        self.anim_explosion = 0

        # -2 offsets explosion's center to (x, y)
        self.explosion_x = x - 2
        self.explosion_y = y - 2

    def loading(self):
        """Allows loading animation to draw"""
        self.anim_loading = 0

    def draw(self, screen):
        """Method that draws every animation if needed"""
        self.anim_counter += 1

        if self.anim_loading < len(CURTAIN):
            for pos in CURTAIN[self.anim_loading]:
                draw_pixel_matrix(screen, pos)
            self.anim_loading += 1

        if self.anim_counter <= self.frame_len:

            # all animation draws go here
            if self.anim_explosion < len(EXPLOSION):

                explosion = offset_sprite(sprite=EXPLOSION[self.anim_explosion],
                                          offset_x=self.explosion_x,
                                          offset_y=self.explosion_y)

                for pos in explosion:
                    draw_pixel_matrix(screen, pos)

        else:
            self.anim_counter = 0
            self.anim_explosion += 1 if self.anim_explosion < len(EXPLOSION) else 0
