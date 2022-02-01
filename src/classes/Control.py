import pygame


class Control:
    def __init__(self):
        self.button_press = False

    def can_press(self, button, keys):
        if keys[button]:
            if not self.button_press:
                return True
        else:
            self.button_press = False

    def hold(self, button, keys, interval):
        pass
