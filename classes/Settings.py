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

        self.settings_buttons = (
            Button([*S_L_UP, 48, 48], '+', 48, self.level_up),
            Button([*S_L_DOWN, 48, 48], '-', 48, self.level_down),
            Button([*S_S_UP, 48, 48], '+', 48, self.speed_up),
            Button([*S_S_DOWN, 48, 48], '-', 48, self.speed_down),
            Button([*S_SW_FPS, 48, 48], 'OFF', 32, self.switch_fps),
            Button([*S_SW_MUSIC, 48, 48], 'OFF', 32, self.switch_music),
            Button([*S_CLOSE, 144, 48], 'ACCEPT', 48, self.close),
        )

        self.settings_buttons[4].text = 'ON' if CONFIG['overall']['fps'] else 'OFF'
        self.settings_buttons[5].text = 'ON' if CONFIG['overall']['music'] else 'OFF'

    def draw(self):
        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))

        frame = [SCREEN_CELL * 3, SCREEN_CELL * 7, WIDTH - 24 * SCREEN_CELL, HEIGHT - 12 * SCREEN_CELL]
        pygame.draw.rect(SCREEN, BACKGROUND, frame)

        draw_text(SCREEN, 'LEVEL', S_LEVEL, 72)
        draw_text(SCREEN, 'SPEED', S_SPEED, 72)
        draw_text(SCREEN, 'FPS', S_FPS, 60)
        draw_text(SCREEN, 'MUSIC', S_MUSIC, 60)

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

    def switch_music(self):
        self.music = 0 if self.music else 1
        if self.music:
            pygame.mixer.music.set_volume(1)
        else:
            pygame.mixer.music.set_volume(0)

        if self.settings_buttons[5].text == 'ON':
            self.settings_buttons[5].text = 'OFF'
        else:
            self.settings_buttons[5].text = 'ON'

    def switch_fps(self):
        if self.settings_buttons[4].text == 'ON':
            self.settings_buttons[4].text = 'OFF'
        else:
            self.settings_buttons[4].text = 'ON'

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
