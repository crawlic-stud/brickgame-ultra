from abc import abstractmethod

import pygame

from src.classes.Animations import Animations
from src.classes.Settings import CONFIG, set_volume
from src.config import MAIN_THEME, ALL_SOUNDS
from src.functions import play_music


class BaseGame:
    def __init__(self, name):
        self.score = 0
        self.bonus_points = 1000
        self.game_over = False
        self.name = name
        self.speed = CONFIG['games'][name]['speed']
        self.level = CONFIG['games'][name]['level']
        self.lives = 3

        play_music(MAIN_THEME)
        if not CONFIG['overall']['music']:
            pygame.mixer.music.set_volume(0)

        set_volume(CONFIG['overall']['volume'])

        self.animation = Animations()
        self.animation.loading()

    @abstractmethod
    def draw_game(self, screen):
        """Method that should be in every game in order to draw all events on screen"""
        pass

    def draw(self, screen):
        self.animation.draw(screen)
        self.draw_game(screen)
