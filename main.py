import sys
from config import *
from functions import draw_text, draw_base_layout, draw_alpha_rect
from classes.Button import Button
import pygame

from classes.Snake import Snake
from classes.Arkanoid import Arkanoid
from classes.SpaceInvaders import SpaceInvaders
from classes.TrafficRacer import TrafficRacer
from classes.TunnelRacer import TunnelRacer

GAMES_LIST = [Snake, Arkanoid, SpaceInvaders, TrafficRacer, TunnelRacer]


class Console:
    def __init__(self):
        self.running = True
        self.current_state = self.previous_state = self.pause
        self.display_fps = False
        self.current_index = 0
        self.game = GAMES_LIST[self.current_index]()

        # buttons
        self.open_settings = Button([*BUTTON_POS, *BUTTON_SIZE], 'SETTINGS', 35,
                                    command=lambda: self.change_state(self.settings))
        self.settings_buttons = (
            Button([*MATRIX_FRAME[-7][2], 48, 48], '+', 48),
            Button([*MATRIX_FRAME[-7][4], 48, 48], '-', 48),
            Button([*MATRIX_FRAME[-7][6], 48, 48], '+', 48),
            Button([*MATRIX_FRAME[-7][8], 48, 48], '-', 48),
            Button([*MATRIX_FRAME[-7][12], 48, 48], 'sw', 48),
            Button([*MATRIX_FRAME[-7][15], 48, 48], 'sw', 48),
            Button([*MATRIX_FRAME[-13][20], 144, 48], 'ACCEPT', 48, lambda: self.change_state(self.previous_state)),
        )

    def run(self):
        while self.running:
            SCREEN.fill(BACKGROUND)
            CLOCK.tick(FPS)

            draw_base_layout(SCREEN, self.game)
            self.open_settings.draw()
            self.game.draw(SCREEN)

            if self.display_fps:
                draw_text(SCREEN, f'{round(CLOCK.get_fps(), 1)} FPS', (0, 0), 20)

            self.current_state()

            pygame.display.update()

    def change_state(self, state):
        if self.current_state != self.settings:
            self.previous_state = self.current_state
        self.current_state = state

    def main(self):
        if self.game.game_over:
            self.change_state(self.over)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_over = True
                    self.change_state(self.pause)

    def pause(self):
        self.game.game_over = True
        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))
        draw_text(SCREEN, 'PAUSE', (0, HEIGHT // 2.5), 100, in_frame=True)
        draw_text(SCREEN, 'press R to restart', (0, HEIGHT // 2.5 + 100), 40, in_frame=True)
        draw_text(SCREEN, '<- SWITCH GAMES ->', (0, HEIGHT // 2.5 + 150), 40, in_frame=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.game.game_over = False
                    PAUSE_SOUND.play()
                    pygame.mixer.music.unpause()
                    self.change_state(self.main)
                if event.key == pygame.K_r:
                    self.game = GAMES_LIST[self.current_index]()
                    self.change_state(self.main)

                if event.key == pygame.K_RIGHT:
                    self.current_index += 1
                    if self.current_index > len(GAMES_LIST) - 1:
                        self.current_index = 0
                    self.game = GAMES_LIST[self.current_index]()
                    pygame.mixer.music.pause()
                    self.game.game_over = True

                if event.key == pygame.K_LEFT:
                    self.current_index -= 1
                    if self.current_index < 0:
                        self.current_index = len(GAMES_LIST) - 1
                    self.game = GAMES_LIST[self.current_index]()
                    self.game.game_over = True
                    pygame.mixer.music.pause()

    def over(self):
        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))
        draw_text(SCREEN, 'GAME OVER', (0, HEIGHT // 2.5), 100, in_frame=True)
        draw_text(SCREEN, f'YOUR SCORE: {str(self.game.score)} pts', (0, HEIGHT // 2.5 + 100), 30, in_frame=True)
        draw_text(SCREEN, 'press any key to CONTINUE ', (0, HEIGHT // 2.5 + 130), 30, in_frame=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.game = GAMES_LIST[self.current_index]()
                self.change_state(self.main)

    def settings(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))

        frame = [SCREEN_CELL * 3, SCREEN_CELL * 7, WIDTH - 24 * SCREEN_CELL, HEIGHT - 12 * SCREEN_CELL]
        pygame.draw.rect(SCREEN, BACKGROUND, frame)

        draw_text(SCREEN, 'LEVEL', MATRIX_FRAME[5][3], 72)
        draw_text(SCREEN, 'SPEED', MATRIX_FRAME[5][7], 72)
        draw_text(SCREEN, 'MUSIC', MATRIX_FRAME[5][12], 60)
        draw_text(SCREEN, 'FPS', MATRIX_FRAME[5][15], 60)

        for button in self.settings_buttons:
            button.draw()


if __name__ == '__main__':
    Console().run()

