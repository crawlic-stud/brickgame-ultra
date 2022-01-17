from classes.Button import Button
from config import *
from functions import draw_text, draw_alpha_rect
import json


with open('config.json', 'r') as f:
    CONFIG = json.load(f)


class Settings:
    def __init__(self, game):
        self.game = game
        self.showing = False
        self.music = CONFIG['overall']['music']
        self.show_fps = CONFIG['overall']['fps']

        # TODO: create all buttons and configure them
        self.settings_buttons = (
            Button([*MATRIX_FRAME[-7][2], 48, 48], '+', 48, self.level_up),
            Button([*MATRIX_FRAME[-7][4], 48, 48], '-', 48, self.level_down),
            Button([*MATRIX_FRAME[-7][6], 48, 48], '+', 48, self.speed_up),
            Button([*MATRIX_FRAME[-7][8], 48, 48], '-', 48, self.speed_down),
            Button([*MATRIX_FRAME[-7][12], 48, 48], 'OFF', 32, self.switch_fps),
            Button([*MATRIX_FRAME[-7][15], 48, 48], 'OFF', 32, self.switch_music),
            Button([*MATRIX_FRAME[-13][20], 144, 48], 'ACCEPT', 48, self.close),
        )

        self.settings_buttons[4].text = 'OFF' if CONFIG['overall']['fps'] else 'ON'
        self.settings_buttons[5].text = 'OFF' if CONFIG['overall']['music'] else 'ON'

    def draw(self):
        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))

        frame = [SCREEN_CELL * 3, SCREEN_CELL * 7, WIDTH - 24 * SCREEN_CELL, HEIGHT - 12 * SCREEN_CELL]
        pygame.draw.rect(SCREEN, BACKGROUND, frame)

        draw_text(SCREEN, 'LEVEL', MATRIX_FRAME[5][3], 72)
        draw_text(SCREEN, 'SPEED', MATRIX_FRAME[5][7], 72)
        draw_text(SCREEN, 'FPS', MATRIX_FRAME[5][12], 60)
        draw_text(SCREEN, 'MUSIC', MATRIX_FRAME[5][15], 60)

        for button in self.settings_buttons:
            button.draw()

    def show(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.showing = False

        self.draw()

    def close(self):
        self.showing = False
        self.save()

    # TODO: implement all switch functions
    def switch_music(self):
        self.music = 0 if self.music else 1
        if self.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        if self.settings_buttons[5].text == 'OFF':
            self.settings_buttons[5].text = 'ON'
        else:
            self.settings_buttons[5].text = 'OFF'

    def switch_fps(self):
        if self.settings_buttons[4].text == 'OFF':
            self.settings_buttons[4].text = 'ON'
        else:
            self.settings_buttons[4].text = 'OFF'

        self.show_fps = 0 if self.show_fps else 1

    def speed_up(self):
        self.game.speed += 1 if self.game.speed < 10 else 0

    def speed_down(self):
        self.game.speed -= 1 if self.game.speed > 1 else 0

    def level_up(self):
        self.game.level += 1 if self.game.level < 10 else 0

    def level_down(self):
        self.game.level -= 1 if self.game.level > 1 else 0

    # TODO: save all changes to config.json file
    def save(self):
        CONFIG['overall']['music'] = self.music
        CONFIG['overall']['fps'] = self.show_fps
        CONFIG['games'][self.game.name]['speed'] = self.game.speed
        CONFIG['games'][self.game.name]['level'] = self.game.level

        with open('config.json', 'w') as file:
            json.dump(CONFIG, file, indent=4)
