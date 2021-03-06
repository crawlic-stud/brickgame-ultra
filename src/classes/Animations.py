from src.functions import offset_sprite, draw_pixel_matrix
from src.sprites import EXPLOSION, CURTAIN, BLINKING, BLINKING_ONCE


class Animations:
    def __init__(self):

        self.anim_counter = 0
        self.frame_len = 3
        self.anim_explosion = len(EXPLOSION) - 1
        self.explosion_x = 0
        self.explosion_y = 0

        self.anim_blinking = len(BLINKING) - 1
        self.blinking_array = []
        self.anim_blink_once = len(BLINKING_ONCE) - 1
        self.blink_once_array = []

        self.anim_loading = len(CURTAIN) - 1

    def blinking(self, pixel_array):
        """Draws blinking pixels"""
        self.anim_blinking = 0

        self.blinking_array = pixel_array

    def blink_once(self, pixel_array):
        """Draws blinking pixels once"""
        self.anim_blink_once = 0

        self.blink_once_array = pixel_array

    def explosion(self, x, y):
        """Draws explosion at certain pos"""
        self.anim_explosion = 0

        # -2 offsets explosion's center to (x, y)
        self.explosion_x = x - 2
        self.explosion_y = y - 2

    def loading(self):
        """Draws loading animation"""
        self.anim_loading = 0

    def draw(self, screen):
        """Method that draws every animation if needed"""

        if self.anim_loading < len(CURTAIN):
            for pos in CURTAIN[self.anim_loading]:
                draw_pixel_matrix(screen, pos)
            self.anim_loading += 1

        if self.anim_blinking < len(BLINKING):
            for pos in self.blinking_array:
                blinking = BLINKING[self.anim_blinking]
                if blinking:
                    draw_pixel_matrix(screen, pos)
            self.anim_blinking += 1
        else:
            self.anim_blinking = 0

        if self.anim_blink_once < len(BLINKING_ONCE):
            for pos in self.blink_once_array:
                blinking = BLINKING_ONCE[self.anim_blink_once]
                if blinking:
                    draw_pixel_matrix(screen, pos)
            self.anim_blink_once += 1

        self.anim_counter += 1
        if self.anim_counter <= self.frame_len:

            if self.anim_explosion < len(EXPLOSION):

                explosion = offset_sprite(sprite=EXPLOSION[self.anim_explosion],
                                          offset_x=self.explosion_x,
                                          offset_y=self.explosion_y)

                for pos in explosion:
                    draw_pixel_matrix(screen, pos)

        else:
            self.anim_counter = 0
            self.anim_explosion += 1 if self.anim_explosion < len(EXPLOSION) else 0
