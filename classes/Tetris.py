import pygame.key

from classes.__init__ import *
from sprites import PIECES, rotate_sprite, convert_with_empty


class Tetris(BaseGame):
    def __init__(self):
        super().__init__('TETRIS')

        self.button_press = False

        self.brick = None
        self.next_brick = TetrisBrick((MATRIX_WIDTH // 2 - 1, -1), random.choice(PIECES))
        self.spawn_brick()
        self.placed_bricks = []

        self.brick_slowness = 5
        self.brick_counter = 0
        self.falling_slowness = 25
        self.falling_counter = 0

        self.rows = [0] * MATRIX_HEIGHT

        self.last_change_counter = 0
        self.time_to_change = 15

    def control(self):
        keys = pygame.key.get_pressed()
        rot = self.brick.rotation

        intersections = [check_intersection_x(self.brick.get_sprite(), self.placed_bricks),
                         check_border_x(self.brick.get_sprite())]

        if keys[pygame.K_LEFT]:
            if 'left' not in intersections:
                self.move_brick(-1)
        elif keys[pygame.K_RIGHT]:
            if 'right' not in intersections:
                self.move_brick(1)
        else:
            self.brick_counter = 0

        if keys[pygame.K_SPACE]:
            if not self.button_press and not self.is_bottom_reached() and self.can_rotate():
                self.brick.rotate(rot + 1)
            self.button_press = True
        else:
            self.button_press = False

        if keys[pygame.K_DOWN]:
            self.falling_slowness = 2
            # self.find_projection()
        else:
            self.falling_slowness = 15

    def move_brick(self, dx):
        if self.brick_counter % self.brick_slowness == 0:
            self.brick.move(dx, 0)
            self.brick_counter = 0
        self.brick_counter += 1

    def spawn_brick(self):
        self.brick = self.next_brick
        self.next_brick = TetrisBrick((MATRIX_WIDTH // 2 - 1, -1), random.choice(PIECES))

    def fall(self):
        if self.is_bottom_reached():
            self.place_bricks()
            return

        if self.falling_counter < self.falling_slowness:
            self.falling_counter += 1
            return

        self.brick.move(0, 1)
        self.falling_counter = 0

    def is_bottom_reached(self):
        return any([check_intersection_y(self.brick.get_sprite(), self.placed_bricks),
                    check_border_y(self.brick.get_sprite()) == 'bottom'])

    def can_rotate(self):
        return not any([check_intersection_y(self.brick.get_sprite(), self.placed_bricks, 2),
                        check_border_y(self.brick.get_sprite()) == 'bottom'])

    def place_bricks(self):
        if self.last_change_counter < self.time_to_change:
            self.last_change_counter += 1
            return

        self.placed_bricks += self.brick.get_sprite()
        self.delete_row()
        self.brick.sprite = []
        self.spawn_brick()
        self.last_change_counter = 0

    def delete_row(self):
        rows = [0] * MATRIX_HEIGHT
        for pixel in self.placed_bricks:
            rows[pixel[1]] += 1
            if pixel[1] < 0:
                self.game_over = True

        for i, row in enumerate(rows):
            if row >= MATRIX_WIDTH:
                upper_blocks = [pos for pos in self.placed_bricks if pos[1] < i]
                lower_blocks = [pos for pos in self.placed_bricks if pos[1] > i]

                self.placed_bricks = offset_sprite(upper_blocks, 0, 1) + lower_blocks
                self.animation.blinking(upper_blocks)

                self.score += self.bonus_points
                self.bonus_points *= 2

        self.bonus_points = 1000

    def find_projection(self):

        # TODO: MAKE IT WORK
        max_brick = [max([pos[0] for pos in self.brick.get_sprite()]), max([pos[1] for pos in self.brick.get_sprite()])]
        placed_under = [pos for pos in self.placed_bricks if pos[0] == max_brick[0]]
        min_y_placed = sorted(placed_under, key=lambda x: x[1])[0][1] if placed_under else MATRIX_HEIGHT - 1
        offset_y = min_y_placed - max_brick[1]

        projection = offset_sprite(self.brick.get_sprite(), 0, offset_y)

        self.animation.blinking(projection)

    def main(self):
        if self.game_over:
            return
        self.control()
        self.fall()

    def draw_game(self, screen):
        self.main()

        draw_next_brick(screen, offset_sprite(self.next_brick.get_sprite(), -MATRIX_WIDTH//2 + 3, 3))

        for pixel in self.brick.get_sprite():
            draw_pixel_matrix(screen, pixel)

        for pixel in self.placed_bricks:
            draw_pixel_matrix(screen, pixel)


class TetrisBrick:
    def __init__(self, pos, brick):
        self.x = pos[0]
        self.y = pos[1]
        self.brick = brick
        self.sprite = offset_sprite2(convert_with_empty(self.brick), self.x, self.y)
        self.rotation = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.update()

    def rotate(self, rotation):
        if rotation > 3:
            rotation = 0
        elif rotation < 0:
            rotation = 3

        self.rotation = rotation

    def update(self):
        self.sprite = offset_sprite2(convert_with_empty(rotate_sprite(self.brick, self.rotation)), self.x, self.y)

    def get_sprite(self):
        return [[pos[0], pos[1]] for pos in self.sprite if pos[2]]
