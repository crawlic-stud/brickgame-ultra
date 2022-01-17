import random
from config import *


def draw_pixel(screen, pos):
    pygame.draw.rect(screen, CELL_COLOR, (pos[0], pos[1], MATRIX_CELL, MATRIX_CELL), 1)
    pygame.draw.rect(screen, CELL_COLOR, (pos[0] + MATRIX_CELL//4, pos[1] + MATRIX_CELL//4, MATRIX_CELL//2, MATRIX_CELL//2))


def draw_pixel_matrix(screen, pos):
    try:
        if pos[0] >= 0 and pos[1] >= 0:
            draw_pixel(screen, MATRIX_FRAME[pos[0]][pos[1]])
    except IndexError:
        pass


def draw_text(screen, text, pos, size, font=FONT, in_frame=False):
    if in_frame:
        font_image = pygame.font.Font(font, size).render(text, True, CELL_COLOR)
        width = font_image.get_size()[0]
        x = FRAME[0] + (FRAME[2] - width) // 2
        screen.blit(font_image, (x, pos[1]))
    else:
        font = pygame.font.Font(font, size)
        screen.blit(font.render(text, True, CELL_COLOR), pos)


def draw_base_layout(screen, game):
    pygame.draw.rect(screen, GRID_COLOR, (GAME_NAME_POS[0], GAME_NAME_POS[1],
                                          text_size(game.name, 40)[0], text_size(game.name, 40)[1]))
    draw_text(screen, game.name, GAME_NAME_POS, 40)
    draw_text(screen, 'SCORE', SCORE_TEXT_POS, 35)
    draw_text(screen, str(game.score).rjust(6, '0'), SCORE_POS, 70, font=SCORE_FONT)
    draw_text(screen, 'SPEED', SPEED_TEXT_POS, 35)
    draw_text(screen, str(game.speed).rjust(2, '0'), SPEED_POS, 70)
    draw_text(screen, 'LEVEL', LEVEL_TEXT_POS, 35)
    draw_text(screen, str(game.level).rjust(2, '0'), LEVEL_POS, 70)
    for rows in MATRIX_FRAME:
        for pos in rows:
            pygame.draw.rect(screen, GRID_COLOR, (pos[0], pos[1], MATRIX_CELL, MATRIX_CELL), 5)
    pygame.draw.rect(screen, CELL_COLOR, FRAME, 2)


def draw_alpha_rect(screen, color, size, pos):
    rectangle = pygame.Surface(size, pygame.SRCALPHA)
    rectangle.fill(color)
    screen.blit(rectangle, pos)


def text_size(text, size, font=FONT):
    font = pygame.font.Font(font, size)
    return font.render(text, True, CELL_COLOR).get_size()


def check_border_x(shape):
    sorted_x = sorted(shape)
    if sorted_x[0][0] <= 0:
        return 'left'
    elif sorted_x[-1][0] >= MATRIX_WIDTH - 1:
        return 'right'


def check_border_y(shape):
    sorted_y = sorted(shape, key=lambda x: x[1])
    if sorted_y[0][1] <= 0:
        return 'top'
    elif sorted_y[-1][1] >= MATRIX_HEIGHT - 1:
        return 'bottom'


def check_intersection_x(shape, obstacle):
    left_border = [[pos[0] - 1, pos[1]] for pos in shape]
    right_border = [[pos[0] + 1, pos[1]] for pos in shape]
    if intersects(left_border, obstacle):
        return 'left'
    elif intersects(right_border, obstacle):
        return 'right'


def check_intersection_y(shape, obstacle):
    top_border = [[pos[0], pos[1] - 1] for pos in shape]
    bottom_border = [[pos[0], pos[1] + 1] for pos in shape]
    if intersects(top_border, obstacle):
        return 'top'
    elif intersects(bottom_border, obstacle):
        return 'bottom'


def play_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1, 0.0)


def intersects(shape1, shape2):
    return [value for value in shape1 if value in shape2]


def sprite_to_bottom(sprite, offset_x=MATRIX_WIDTH//3):
    return [[i[0] + offset_x, i[1] + (MATRIX_HEIGHT - sprite[-1][1] - 1)] for i in sprite]


def offset_sprite(sprite, offset_x, offset_y):
    return [[i[0] + offset_x, i[1] + offset_y] for i in sprite]


def shuffle_poses(length=6):
    holes = random.randint(3, length-2)
    array = [0 for _ in range(holes)] + [1 for _ in range(length - holes)]
    random.shuffle(array)
    return array


if __name__ == '__main__':
    print()
