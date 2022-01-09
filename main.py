from settings import *
from functions import draw_text, draw_base_layout, draw_alpha_rect
from classes.Button import Button

from classes.Snake import Snake
from classes.Arkanoid import Arkanoid
from classes.SpaceInvaders import SpaceInvaders
from classes.TrafficRacer import TrafficRacer
from classes.TunnelRacer import TunnelRacer

GAMES_LIST = [Snake, Arkanoid, SpaceInvaders, TrafficRacer, TunnelRacer]
current_game = TunnelRacer
current_index = 0
settings_button = Button([*BUTTON_POS, *BUTTON_SIZE], 'SETTINGS', 35)


def main(game):
    running = True
    while running:
        SCREEN.fill(BACKGROUND)
        CLOCK.tick(FPS)

        pygame.display.set_caption(f'{round(CLOCK.get_fps(), 1)} FPS')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game.game_over = True
                    pause(game)

        if game.game_over:
            game_over(game)

        draw_base_layout(SCREEN, game)
        settings_button.draw()
        game.draw(SCREEN)

        pygame.display.update()


def pause(game):
    global current_game, current_index
    pausing = True
    PAUSE_SOUND.play()
    pygame.mixer.music.pause()
    while pausing:
        SCREEN.fill(BACKGROUND)
        CLOCK.tick(FPS)

        draw_base_layout(SCREEN, game)
        settings_button.draw()
        game.draw(SCREEN)

        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))
        draw_text(SCREEN, 'PAUSE', (0, HEIGHT//2.5), 100, in_frame=True)
        draw_text(SCREEN, 'press R to restart', (0, HEIGHT//2.5 + 100), 40, in_frame=True)
        draw_text(SCREEN, '<- SWITCH GAMES ->', (0, HEIGHT // 2.5 + 150), 40, in_frame=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    pausing = False
                    game.game_over = False
                    PAUSE_SOUND.play()
                    pygame.mixer.music.unpause()
                    main(game)
                if event.key == pygame.K_r:
                    pausing = False
                    main(game=current_game())

                if event.key == pygame.K_RIGHT:
                    current_index += 1
                    if current_index > len(GAMES_LIST) - 1:
                        current_index = 0
                    current_game = GAMES_LIST[current_index]
                    game = current_game()
                    pygame.mixer.music.pause()
                    game.game_over = True

                if event.key == pygame.K_LEFT:
                    current_index -= 1
                    if current_index < 0:
                        current_index = len(GAMES_LIST) - 1
                    current_game = GAMES_LIST[current_index]
                    game = current_game()
                    pygame.mixer.music.pause()
                    game.game_over = True

        pygame.display.update()


def game_over(game):
    pausing = True
    GAME_OVER_SOUND.play()
    pygame.mixer.music.stop()
    while pausing:
        SCREEN.fill(BACKGROUND)
        CLOCK.tick(FPS)

        draw_base_layout(SCREEN, game)
        settings_button.draw()
        game.draw(SCREEN)
        draw_alpha_rect(SCREEN, BACKLIGHT_COLOR, (FRAME[2], FRAME[3]), (FRAME[0], FRAME[1]))
        draw_text(SCREEN, 'GAME OVER', (0, HEIGHT // 2.5), 100, in_frame=True)
        draw_text(SCREEN, f'YOUR SCORE: {str(game.score)} pts', (0, HEIGHT // 2.5 + 100), 30, in_frame=True)
        draw_text(SCREEN, 'press any key to CONTINUE ', (0, HEIGHT // 2.5 + 130), 30, in_frame=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main(game=current_game())

        pygame.display.update()


if __name__ == '__main__':
    main(game=current_game())
