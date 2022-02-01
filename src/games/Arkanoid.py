from src.games.__init__ import *
import random


class Arkanoid(BaseGame):
    def __init__(self):
        super().__init__('ARKANOID')

        self.platform_length = 5
        self.platform = [[PLATFORM_DEFAULT_POS + i, MATRIX_HEIGHT - 1] for i in range(self.platform_length)]

        self.slowness = 5
        self.ball_pos = BALL_DEFAULT_POS
        self.ball_vel = [-1, -1]
        self.ball_speed = 0

        self.bonus_points = 100

        self.bricks = [[random.randint(0, self.level) for _ in range(BRICK_ROWS)] for _ in range(MATRIX_WIDTH)]
        self.button_press = 0

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and check_border_x(self.platform) != 'right':
            if self.button_press % self.slowness == 0:
                self.move_platform(1)
            self.button_press += 1
        elif keys[pygame.K_LEFT] and check_border_x(self.platform) != 'left':
            if self.button_press % self.slowness == 0:
                self.move_platform(-1)
            self.button_press += 1

        elif keys[pygame.K_q]:
            self.new_brick_line()
        elif keys[pygame.K_e]:
            self.remove_brick_line()
        else:
            self.button_press = 0

    def move_platform(self, direction):
        new_platform = [[pixel[0] + direction, pixel[1]] for pixel in self.platform]
        self.platform = new_platform

    def brick_collision(self):
        ball_x, ball_y = self.ball_pos

        for x, bricks in enumerate(self.bricks):
            for y, brick in enumerate(bricks):
                if not brick:
                    continue

                x_border = [ball_x - 1, ball_x + 1]
                y_border = [ball_y - 1, ball_y + 1]

                if ball_x == x and y in y_border:
                    self.ball_vel[1] *= -1
                elif x in x_border and ball_y == y:
                    self.ball_vel[0] *= -1
                elif not (x in x_border and y in y_border):
                    continue

                self.hit(x, y)

    def hit(self, x, y):
        BOUNCE_SOUND.play(fade_ms=100)
        self.bricks[x][y] = 0
        self.score += self.bonus_points
        self.bonus_points += 100

    def ball_collision(self):
        if self.ball_pos[0] == 0 or self.ball_pos[0] == MATRIX_WIDTH - 1:
            self.ball_vel[0] *= -1
        if self.ball_pos[1] == 0:
            self.ball_vel[1] *= -1
        elif self.ball_pos[1] >= MATRIX_HEIGHT - 1:
            self.animation.explosion(*self.ball_pos)
            self.game_over = True

        platform_level = MATRIX_HEIGHT - 2
        platform_x = [pos[0] for pos in self.platform]
        if self.ball_pos[1] == platform_level:
            if self.ball_pos[0] in platform_x:
                self.ball_vel[1] *= -1
            elif self.ball_pos[0] == platform_x[0] - 1:
                self.ball_vel = [-1, -1]
            elif self.ball_pos[0] == platform_x[-1] + 1:
                self.ball_vel = [1, -1]

        self.bonus_points = 100

    def ball_in_border(self):
        if self.ball_pos[0] <= 0:
            self.ball_pos[0] = 0
        if self.ball_pos[0] >= MATRIX_WIDTH - 1:
            self.ball_pos[0] = MATRIX_WIDTH - 1
        if self.ball_pos[1] <= 0:
            self.ball_pos[1] = 0

    def move_ball(self):
        self.ball_speed += 1
        if self.ball_speed >= self.slowness:
            new_ball_pos = [self.ball_pos[0] + self.ball_vel[0],
                            self.ball_pos[1] + self.ball_vel[1]]
            self.ball_pos = new_ball_pos
            self.ball_speed = 0

    def new_brick_line(self):
        self.bricks = [[random.randint(0, self.level)] + bricks for bricks in self.bricks]

    def remove_brick_line(self):
        self.bricks = [bricks[:-1] for bricks in self.bricks]

    def main(self):
        if self.game_over:
            return

        brick_line = [bricks[-1] for bricks in self.bricks]
        if not any(brick_line):
            self.remove_brick_line()

        active_bricks = [brick for bricks in self.bricks for brick in bricks if brick]
        if len(active_bricks) < 100:
            self.new_brick_line()

        if len(self.bricks[0]) >= MATRIX_HEIGHT - 4:
            self.game_over = True

        self.ball_collision()
        self.brick_collision()
        self.move_ball()
        self.ball_in_border()
        self.control()

    def draw_game(self, screen):
        self.main()
        for pixel in self.platform:
            draw_pixel_matrix(screen, pixel)

        draw_pixel_matrix(screen, self.ball_pos)

        for i, bricks in enumerate(self.bricks):
            for j, brick in enumerate(bricks):
                if not brick:
                    continue
                draw_pixel_matrix(screen, (i, j))
