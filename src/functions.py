import random
from math import sqrt

from src.config import *


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
    draw_text(screen, str(game.speed).rjust(2, '0'), SPEED_POS, 70, font=SCORE_FONT)
    draw_text(screen, 'LEVEL', LEVEL_TEXT_POS, 35)
    draw_text(screen, str(game.level).rjust(2, '0'), LEVEL_POS, 70, font=SCORE_FONT)
    for rows in MATRIX_FRAME:
        for pos in rows:
            pygame.draw.rect(screen, GRID_COLOR, (pos[0], pos[1], MATRIX_CELL, MATRIX_CELL), 5)
    pygame.draw.rect(screen, CELL_COLOR, FRAME, 2)


def draw_alpha_rect(screen, color, size, pos):
    rectangle = pygame.Surface(size, pygame.SRCALPHA)
    rectangle.fill(color)
    screen.blit(rectangle, pos)


def next_brick_layout(screen):
    draw_text(screen, 'NEXT', NEXT_BRICK_TEXT, 35)

    for rows in NEXT_BRICK_MATRIX:
        for row in rows:
            pygame.draw.rect(screen, GRID_COLOR, [row[0], row[1], MATRIX_CELL, MATRIX_CELL], 5)

    pygame.draw.rect(screen, CELL_COLOR,
                     [*NEXT_BRICK_POS, BRICK_MATRIX_WIDTH * MATRIX_CELL, BRICK_MATRIX_WIDTH * MATRIX_CELL], 2)


def draw_next_brick(screen, brick):
    next_brick_layout(screen)
    for pixel in brick:
        draw_pixel(screen, NEXT_BRICK_MATRIX[pixel[0]][pixel[1]])


def text_size(text, size, font=FONT):
    font = pygame.font.Font(font, size)
    return font.render(text, True, CELL_COLOR).get_size()


def get_shape_pos(shape):
    x = sorted(shape)[0]
    y = sorted(shape, key=lambda i: i[1])[1]
    return x, y


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


def check_intersection_x(shape, obstacle, size=1):
    right_border = [[pos[0] + size, pos[1]] for pos in shape]
    left_border = [[pos[0] - size, pos[1]] for pos in shape]
    if intersects(left_border, obstacle):
        return 'left'
    elif intersects(right_border, obstacle):
        return 'right'


def check_intersection_y(shape, obstacle, size=1):
    bottom_border = [[pos[0], pos[1] + size] for pos in shape]
    top_border = [[pos[0], pos[1] - size] for pos in shape]
    if intersects(top_border, obstacle):
        return 'top'
    elif intersects(bottom_border, obstacle):
        return 'bottom'


def intersection_circle(shape, size=1):
    borders = [[pos[0] + i, pos[1] + j] for i in range(-size, size+1) for j in range(-size, size+1) for pos in shape]
    return borders


def check_all_intersections(shape, obstacles):
    intersection_x = [check_intersection_x(shape, obstacle) for obstacle in obstacles]
    intersection_y = [check_intersection_y(shape, obstacle) for obstacle in obstacles]

    intersections = intersection_x + intersection_y
    intersections = [i for i in intersections if i]

    return intersections


def all_intersections_ai(shape, obstacles, size=1):
    intersection_x = [check_intersection_x(shape, obstacle, size) for obstacle in obstacles]
    intersection_y = [check_intersection_y(shape, obstacle, size) for obstacle in obstacles]

    intersections = intersection_x + intersection_y
    intersections = [i for i in intersections if i]

    return intersections


def calculate_movement(intersections):
    """Returns possible direction based on intersections, but can't handle if there's no intersections"""
    dx, dy = 0, 0

    if 'right' in intersections:
        dx = -1
    elif 'left' in intersections:
        dx = 1
    elif 'top' in intersections:
        dy = 1
    elif 'bottom' in intersections:
        dy = -1

    if 'left' in intersections and 'right' in intersections:
        if 'top' in intersections:
            dy = 1
        elif 'bottom' in intersections:
            dy = -1

    if 'top' in intersections and 'bottom' in intersections:
        if 'right' in intersections:
            dx = -1
        elif 'left' in intersections:
            dx = 1

    if 'right' in intersections and 'left' in intersections and 'top' in intersections and 'bottom' in intersections:
        dx, dy = 0, 0

    return dx, dy


def calculate_facing(direction):
    dx, dy = direction
    facing = 0
    if dx == 1:
        facing = 1
    if dx == -1:
        facing = 3
    if dy == 1:
        facing = 2
    return facing


def calculate_direction(facing):
    if facing == 0:
        direction = (0, -1)
    elif facing == 2:
        direction = (0, 1)
    elif facing == 1:
        direction = (1, 0)
    else:
        direction = (-1, 0)
    return direction


def play_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1, 0.0)


def intersects(shape1, shape2):
    return [value for value in shape1 if value in shape2]


def sprite_to_bottom(sprite, offset_x=MATRIX_WIDTH//3):
    return [[i[0] + offset_x, i[1] + (MATRIX_HEIGHT - sprite[-1][1] - 1)] for i in sprite]


def offset_sprite(sprite, offset_x, offset_y):
    return [[i[0] + offset_x, i[1] + offset_y] for i in sprite]


def offset_sprite2(sprite, offset_x, offset_y):
    for i, _ in enumerate(sprite):
        sprite[i][0] += offset_x
        sprite[i][1] += offset_y
    return sprite


def shuffle_poses(length=6):
    holes = random.randint(3, length-2)
    array = [0 for _ in range(holes)] + [1 for _ in range(length - holes)]
    random.shuffle(array)
    return array


def two_point_distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


if __name__ == '__main__':
    print(intersection_circle([[0, 1], [1, 0], [1, 1], [0, 0]]))
