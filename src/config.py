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
BOUNCE_SOUND.set_volume(0.1)

ALL_SOUNDS = [LEVEL_UP_SOUND,
              PICK_UP_SOUND,
              HIT_SOUND,
              BOUNCE_SOUND,
              GAME_OVER_SOUND,
              PAUSE_SOUND,
              MOVEMENT_SOUND,
              PEW_SOUND_1,
              PEW_SOUND_2,
              ENEMY_DEATH_SOUND]

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
SPEED_TEXT_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 22
SPEED_POS = SCREEN_CELL * 52, HEIGHT - SCREEN_CELL * 24
LEVEL_TEXT_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 15
LEVEL_POS = SCREEN_CELL * 52, HEIGHT - SCREEN_CELL * 17

BUTTON_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 6
BUTTON_SIZE = SCREEN_CELL * 13, SCREEN_CELL * 4

NEXT_BRICK_POS = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 45
NEXT_BRICK_TEXT = SCREEN_CELL * 43, HEIGHT - SCREEN_CELL * 48
BRICK_MATRIX_WIDTH = 7
NEXT_BRICK_MATRIX = np.array([[(i, j) for j in range(NEXT_BRICK_POS[1], NEXT_BRICK_POS[1] + BRICK_MATRIX_WIDTH * MATRIX_CELL, MATRIX_CELL)]
                              for i in range(NEXT_BRICK_POS[0], NEXT_BRICK_POS[0] + BRICK_MATRIX_WIDTH * MATRIX_CELL, MATRIX_CELL)])

# settings
# text
text_indent = 8

S_LEVEL = text_indent * SCREEN_CELL, 9 * SCREEN_CELL
S_SPEED = text_indent * SCREEN_CELL, 17 * SCREEN_CELL
S_FPS = text_indent * SCREEN_CELL, 29 * SCREEN_CELL
S_MUSIC = text_indent * SCREEN_CELL, 35 * SCREEN_CELL
S_VOLUME = text_indent * SCREEN_CELL, 41 * SCREEN_CELL
S_VOLUME_STATUS = (text_indent + 15) * SCREEN_CELL, 41 * SCREEN_CELL

# buttons
button_indent = 30

S_L_UP = button_indent * SCREEN_CELL, 7 * SCREEN_CELL
S_L_DOWN = button_indent * SCREEN_CELL, 11 * SCREEN_CELL
S_S_UP = button_indent * SCREEN_CELL, 15 * SCREEN_CELL
S_S_DOWN = button_indent * SCREEN_CELL, 19 * SCREEN_CELL
S_SW_FPS = button_indent * SCREEN_CELL, 28 * SCREEN_CELL
S_SW_MUSIC = button_indent * SCREEN_CELL, 34 * SCREEN_CELL
S_VOL_UP = button_indent * SCREEN_CELL, 40 * SCREEN_CELL
S_VOL_DOWN = (text_indent + 11) * SCREEN_CELL, 40 * SCREEN_CELL
S_CLOSE = button_indent//2 * SCREEN_CELL, 50 * SCREEN_CELL

# colors
BACKGROUND = (90, 90, 85)
CELL_COLOR = (10, 10, 10)
GRID_COLOR = tuple([i - 5 for i in BACKGROUND])
SHADE_COLOR = (0, 0, 0, 128)
BACKLIGHT_COLOR = (255, 255, 255, 48)

# snake
SNAKE_DEFAULT_POS = [10, 15]

# arkanoid
BRICK_ROWS = MATRIX_HEIGHT - 15
BRICKS_FRAME = np.zeros((MATRIX_WIDTH, BRICK_ROWS))
PLATFORM_DEFAULT_POS = 4
BALL_DEFAULT_POS = [PLATFORM_DEFAULT_POS + 1, MATRIX_HEIGHT - 3]

# space invaders
MAX_ROW = 18

# traffic racer
BASIC_WAVE = [i for i in range(1, 19, 3)]
RIGHT_BORDER = [[MATRIX_WIDTH - 1, i] for i in range(MATRIX_HEIGHT - 5, MATRIX_HEIGHT)]
LEFT_BORDER = [[0, i] for i in range(MATRIX_HEIGHT - 5, MATRIX_HEIGHT)]
PLAYER_CAR_MOVES = [0, 3, 6, 11, 14, 17]
SLOWNESS_LIST = [0, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2]

# tanks
SPAWN_POINTS = [(3, MATRIX_HEIGHT - 7), (MATRIX_WIDTH - 5, MATRIX_HEIGHT - 7), (3, 3), (MATRIX_WIDTH - 5, 3),
                (3, MATRIX_HEIGHT // 2), (MATRIX_WIDTH - 5, MATRIX_HEIGHT // 2)]
