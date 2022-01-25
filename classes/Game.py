import pygame

from classes.Animations import Animations
from classes.Settings import CONFIG
from config import MAIN_THEME
from functions import play_music


class BaseGame:
    def __init__(self, name):
        self.score = 0
        self.bonus_points = 1000
        self.game_over = False
        self.name = name
        self.speed = CONFIG['games'][name]['speed']
        self.level = CONFIG['games'][name]['level']

        play_music(MAIN_THEME)
        if not CONFIG['overall']['music']:
            pygame.mixer.music.pause()

        self.animation = Animations()
        self.animation.loading()

    def draw_game(self, screen):
        """Method that should be in every game in order to draw all events on screen"""
        pass
    
    def draw(self, screen):
        self.animation.draw(screen)
        self.draw_game(screen)
