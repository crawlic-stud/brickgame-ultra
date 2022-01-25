from classes.__init__ import *


class Snake(BaseGame):
    def __init__(self):
        super().__init__('SNAKE')
        self.x, self.y = SNAKE_DEFAULT_POS
        self.vel = [1, 0]

        self.apple_pos = [random.randrange(MATRIX_WIDTH), random.randrange(MATRIX_HEIGHT)]
        self.apple_show = 0

        self.slowness = 10
        self.speed_counter = 0

        self.snake = [[self.x, self.y]]
        self.length = 2

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.vel != [0, 1]:
            self.vel = [0, -1]
        elif keys[pygame.K_DOWN] and self.vel != [0, -1]:
            self.vel = [0, 1]
        elif keys[pygame.K_RIGHT] and self.vel != [-1, 0]:
            self.vel = [1, 0]
        elif keys[pygame.K_LEFT] and self.vel != [1, 0]:
            self.vel = [-1, 0]

    def collide_tail(self):
        for segment in self.snake[-self.length:-1]:
            if [self.x, self.y] == segment:
                HIT_SOUND.play()
                self.snake = []
                self.animation.explosion(self.x, self.y)
                self.game_over = True

    def collide_apple(self):
        self.apple_show += 1
        if self.apple_show > 7:
            self.apple_show = 0

        if [self.x, self.y] == self.apple_pos:
            PICK_UP_SOUND.play(fade_ms=100)
            while self.apple_pos in self.snake[-self.length:]:
                self.reset_apple()
            self.length += 1
            self.score += 1000 + self.bonus_points
            self.bonus_points = 1000
            self.apply_speed()

    def reappear(self):
        if self.x >= MATRIX_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = MATRIX_WIDTH - 1
        if self.y >= MATRIX_HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = MATRIX_HEIGHT - 1

    def apply_speed(self):
        if self.length % (120 // self.level) == 0:
            LEVEL_UP_SOUND.play()
            self.slowness -= 1
            self.speed += 1
        if self.slowness <= 5:
            self.slowness = 5
        if self.speed >= 5:
            self.speed = 5

    def move(self):
        self.speed_counter += 1
        if self.speed_counter >= self.slowness:
            self.x += self.vel[0]
            self.y += self.vel[1]
            self.reappear()

            self.bonus_points -= 10
            if self.bonus_points <= 0:
                self.bonus_points = 0
            self.snake.append([self.x, self.y])
            self.snake = self.snake[-self.length:]
            self.collide_tail()
            self.speed_counter = 0

    def reset_apple(self):
        self.apple_pos = [random.randrange(MATRIX_WIDTH), random.randrange(MATRIX_HEIGHT)]

    def main(self):
        if self.game_over:
            return

        self.control()
        self.collide_apple()
        self.move()

    def draw_game(self, screen):
        self.main()

        if self.apple_show:
            draw_pixel_matrix(screen, self.apple_pos)

        for segment in self.snake:
            draw_pixel_matrix(screen, segment)
