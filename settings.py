import numpy as np
import pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()


SIZE = WIDTH, HEIGHT = 720, 720
FPS = 60
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption('TETRIS MT1997')

SCREEN_CELL = 12
MATRIX_CELL = 24

# fonts
FONT = 'essentials/fonts/digital-7.ttf'
SCORE_FONT = 'essentials/fonts/digital-7 (mono).ttf'

# sounds
LEVEL_UP_SOUND = pygame.mixer.Sound('essentials/sounds/level_up.wav')
PICK_UP_SOUND = pygame.mixer.Sound('essentials/sounds/pickup.wav')
HIT_SOUND = pygame.mixer.Sound('essentials/sounds/hit_sound.wav')
BOUNCE_SOUND = pygame.mixer.Sound('essentials/sounds/ball_bounce.wav')
GAME_OVER_SOUND = pygame.mixer.Sound('essentials/sounds/game_over.wav')
PAUSE_SOUND = pygame.mixer.Sound('essentials/sounds/pause.wav')
MOVEMENT_SOUND = pygame.mixer.Sound('essentials/sounds/movement.wav')
PEW_SOUND_1 = pygame.mixer.Sound('essentials/sounds/shoot1.wav')
PEW_SOUND_2 = pygame.mixer.Sound('essentials/sounds/shoot2.wav')
ENEMY_DEATH_SOUND = pygame.mixer.Sound('essentials/sounds/enemy_explosion.wav')
ENEMY_DEATH_SOUND.set_volume(0.1)
GAME_OVER_SOUND.set_volume(0.1)

# music
SECOND_THEME = 'essentials/music/second_theme.wav'
MAIN_THEME = 'essentials/music/main_song.wav'

# frame settings
FRAME = [SCREEN_CELL,  # frame X
         SCREEN_CELL * 4,  # frame Y
         WIDTH - 20 * SCREEN_CELL,  # frame width
         HEIGHT - 6 * SCREEN_CELL]    # frame height

MATRIX_FRAME = np.array([[(i, j) for j in range(FRAME[1], FRAME[1] + FRAME[3], MATRIX_CELL)]
                         for i in range(FRAME[0], FRAME[0] + FRAME[2], MATRIX_CELL)])
MATRIX_WIDTH = len(MATRIX_FRAME)
MATRIX_HEIGHT = len(MATRIX_FRAME[0])

# all info positions displayed on main screen
SCORE_POS = SCREEN_CELL * 43, SCREEN_CELL // 2
SCORE_TEXT_POS = SCORE_POS[0] - SCREEN_CELL * 8.5, SCORE_POS[1] + SCREEN_CELL // 3
GAME_NAME_POS = SCREEN_CELL, SCREEN_CELL
SPEED_TEXT_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 25
SPEED_POS = SCREEN_CELL * 52, HEIGHT - SCREEN_CELL * 27
LEVEL_TEXT_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 15
LEVEL_POS = SCREEN_CELL * 52, HEIGHT - SCREEN_CELL * 17
BUTTON_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 6
BUTTON_SIZE = SCREEN_CELL * 13, SCREEN_CELL * 4

# colors
BACKGROUND = (90, 90, 85)
CELL_COLOR = (10, 10, 10)
GRID_COLOR = tuple([i - 5 for i in BACKGROUND])
SHADE_COLOR = (0, 0, 0, 128)
BACKLIGHT_COLOR = (255, 255, 255, 48)

# snake
SNAKE_DEFAULT_POS = [10, 5]

# arkanoid
BRICK_ROWS = MATRIX_HEIGHT - 15
BRICKS_FRAME = np.zeros((MATRIX_WIDTH, BRICK_ROWS))
PLATFORM_DEFAULT_POS = 4
BALL_DEFAULT_POS = [PLATFORM_DEFAULT_POS + 1, MATRIX_HEIGHT - 3]

# space invaders
BOSS = [[5, 0], [11, 0]] + [[i, 1] for i in range(3, 14)]\
       + [[2, 2], [3, 2]] + [[i, 2] for i in range(5, 12)] + [[13, 2], [14, 2]]\
       + [[2, 3], [3, 3]] + [[i, 3] for i in range(6, 11)] + [[13, 3], [14, 3]]\
       + [[1, 4], [2, 4], [3, 4]] + [[i, 4] for i in range(7, 10)] + [[13, 4], [14, 4], [15, 4]]\
       + [[i, 5] for i in range(1, 16)]\
       + [[1, 6], [2, 6]] + [[i, 6] for i in range(3, 14, 2)] + [[14, 6], [15, 6]]\
       + [[i, 7] for i in range(17)]\
       + [[i, 8] for i in range(17)]\
       + [[1, 9], [5, 9], [7, 9], [9, 9], [11, 9], [15, 9]]\
       + [[2, 10], [4, 10], [12, 10], [14, 10]]

MAX_ROW = 18

# racing
BASIC_WAVE = [i for i in range(1, 19, 3)]
RIGHT_BORDER = [[MATRIX_WIDTH - 1, i] for i in range(MATRIX_HEIGHT - 5, MATRIX_HEIGHT)]
LEFT_BORDER = [[0, i] for i in range(MATRIX_HEIGHT - 5, MATRIX_HEIGHT)]
PLAYER_CAR_MOVES = [0, 3, 6, 11, 14, 17]
SLOWNESS_LIST = [0, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
