import random

from classes.__init__ import *
from sprites import CAR, convert


class TunnelRacer(BaseGame):
    def __init__(self):
        super().__init__('TUNNEL RACER')
        self.car = offset_sprite(CAR, offset_x=MATRIX_WIDTH//2 - 1, offset_y=MATRIX_HEIGHT - 6)

        self.path_width = 8
        self.first_row = (' ' * self.path_width).center(MATRIX_WIDTH, 'x')
        self.path = offset_sprite(convert([self.first_row]), offset_x=0, offset_y=MATRIX_HEIGHT-1)

        for _ in range(MATRIX_HEIGHT):
            self.create_path()

        self.slowness = 20 // self.speed
        self.car_speed_counter = 0
        self.button_press = False

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not self.button_press:
                self.move_player(-1)
                self.button_press = True
        elif keys[pygame.K_RIGHT]:
            if not self.button_press:
                self.move_player(1)
                self.button_press = True
        else:
            self.button_press = False

        if keys[pygame.K_UP]:
            self.slowness = 2
        else:
            self.slowness = 20 // self.speed

    def move_player(self, direction):
        self.car = offset_sprite(self.car, offset_x=direction, offset_y=0)

    def collision(self):
        if intersects(self.car, self.path):
            self.animation.explosion(*self.car[0])
            self.car = []
            self.game_over = True

    def create_path(self):
        prev_row = self.path[:MATRIX_WIDTH-self.path_width]
        right_wall = prev_row[len(prev_row)//2]
        left_wall = prev_row[len(prev_row)//2 - 1]

        if random.randint(0, 10 // self.level):
            new_row = offset_sprite(prev_row, offset_x=0, offset_y=-1)
        else:
            offset = random.choice([-1, 1])
            if offset == -1 and left_wall[0] == 2:
                offset = random.randint(0, 1)
            elif offset == 1 and right_wall[0] == MATRIX_WIDTH - 3:
                offset = random.randint(-1, 0)
            new_row = offset_sprite(prev_row, offset_x=offset, offset_y=-1)

        for i, point in enumerate(new_row):
            if point[0] >= MATRIX_WIDTH:
                new_row[i][0] = point[0] - MATRIX_WIDTH
            elif point[0] < 0:
                new_row[i][0] = point[0] + MATRIX_WIDTH

        self.path = new_row + self.path

    def move_path(self):
        self.car_speed_counter += 1
        if self.car_speed_counter >= self.slowness:
            self.create_path()
            self.path = offset_sprite(self.path, offset_x=0, offset_y=1)
            self.car_speed_counter = 0

    def remove_path(self):
        for i, point in enumerate(self.path):
            if point[1] > MATRIX_HEIGHT:
                self.path.remove(self.path[i])

    def main(self):
        if self.game_over:
            return
        self.control()
        self.collision()
        self.move_path()
        self.remove_path()

    def draw_game(self, screen):
        self.main()
        for pixel in self.car:
            draw_pixel_matrix(screen, pixel)

        for pixel in self.path:
            draw_pixel_matrix(screen, pixel)
