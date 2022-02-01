import sys

from src.config import *
from src.functions import draw_text, draw_base_layout, draw_alpha_rect, draw_next_brick
from src.sprites import BORDER_SMALL

from src.classes.Button import Button
from src.classes.Settings import Settings

from src.games.Snake import Snake
from src.games.Arkanoid import Arkanoid
from src.games.SpaceInvaders import SpaceInvaders
from src.games.TrafficRacer import TrafficRacer
from src.games.TunnelRacer import TunnelRacer
from src.games.TanksBattle import TanksBattle
from src.games.Tetris import Tetris

GAMES_LIST = [Snake, Arkanoid, SpaceInvaders, TrafficRacer, TunnelRacer, TanksBattle, Tetris]


class Console:
    def __init__(self):
        self.running = True
        self.current_state = self.previous_state = self.pause
        self.current_index = 0
        self.game = GAMES_LIST[self.current_index]()

        self.settings = Settings(self.game)
        self.settings_button = Button([*BUTTON_POS, *BUTTON_SIZE], 'SETTINGS', 35, self.settings_switch)

    def run(self):
        while self.running:
            SCREEN.fill(BACKGROUND)
            CLOCK.tick(FPS)

            draw_base_layout(SCREEN, self.game)
            self.settings_button.draw()
            self.game.draw(SCREEN)
            if self.current_index != 6:
                draw_next_brick(SCREEN, BORDER_SMALL)

            if self.settings.show_fps:
                draw_text(SCREEN, f'{round(CLOCK.get_fps(), 1)} FPS', (0, 0), 20)

            self.current_state()

            if self.settings.showing:
                self.settings.show()
                self.change_state(self.pause)

            pygame.display.update()

    def reset(self):
        self.game = GAMES_LIST[self.current_index]()
        self.settings = Settings(self.game)

    def change_state(self, state):
        self.current_state = state

    def settings_switch(self):
        self.settings.showing = not self.settings.showing

    def main(self):
        if self.game.game_over:
            self.change_state(self.over)
            GAME_OVER_SOUND.play()

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
                    self.reset()
                    self.change_state(self.main)

                if event.key == pygame.K_RIGHT:
                    self.current_index += 1
                    if self.current_index > len(GAMES_LIST) - 1:
                        self.current_index = 0
                    self.reset()
                    self.game.game_over = True

                if event.key == pygame.K_LEFT:
                    self.current_index -= 1
                    if self.current_index < 0:
                        self.current_index = len(GAMES_LIST) - 1
                    self.reset()
                    self.game.game_over = True

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
                self.reset()
                self.change_state(self.main)


if __name__ == '__main__':
    Console().run()

