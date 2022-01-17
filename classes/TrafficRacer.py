from classes.__init__ import *
from sprites import CAR, BIG_CAR, CAR_REVERT, LINE


class TrafficRacer(BaseGame):
    def __init__(self):
        super().__init__('TRAFFIC RACER')
        self.current_pos = 4
        self.car = offset_sprite(CAR, offset_x=PLAYER_CAR_MOVES[self.current_pos], offset_y=MATRIX_HEIGHT - 6)
        self.traffic = []
        self.oncoming_traffic = []
        self.line = offset_sprite(LINE, offset_x=MATRIX_WIDTH // 2 - 1, offset_y=-3)
        self.button_press = False
        self.cars_slowness = SLOWNESS_LIST[self.speed]
        self.cars_speed_counter = 0
        self.spawn_timer = 0
        self.spawn_time = 60 * self.cars_slowness // self.level
        self.spawn_cars()

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if check_border_x(self.car) != 'left' and not self.button_press:
                self.move_player_car(-1)
                self.button_press = True
        elif keys[pygame.K_RIGHT]:
            if check_border_x(self.car) != 'right' and not self.button_press:
                self.move_player_car(1)
                self.button_press = True
        else:
            self.button_press = False

        if keys[pygame.K_UP]:
            self.cars_slowness = SLOWNESS_LIST[-1]
            self.spawn_time = 180 // self.level
        else:
            self.cars_slowness = SLOWNESS_LIST[self.speed]
            self.spawn_time = 60 * self.cars_slowness // self.level

    def move_player_car(self, direction):
        self.current_pos += direction

        if self.current_pos <= 0:
            self.current_pos = 0
        elif self.current_pos >= PLAYER_CAR_MOVES[-1]:
            self.current_pos = PLAYER_CAR_MOVES[-1]

        new_x = PLAYER_CAR_MOVES[self.current_pos]
        self.car = offset_sprite(CAR, offset_x=new_x, offset_y=MATRIX_HEIGHT - 6)

    def spawn_cars(self):
        poses = shuffle_poses()
        spawn_range = 4, 5
        wave_1 = [offset_sprite(CAR, offset_x=PLAYER_CAR_MOVES[-3:][i], offset_y=-random.randint(*spawn_range))
                  for i, pose in enumerate(poses[-3:]) if pose]
        wave_2 = [offset_sprite(CAR_REVERT, offset_x=PLAYER_CAR_MOVES[:-3][i], offset_y=-random.randint(*spawn_range))
                  for i, pose in enumerate(poses[:-3]) if pose]
        self.traffic += wave_1
        self.oncoming_traffic += wave_2
        self.score += 100

    def move_cars(self):
        self.cars_speed_counter += 1

        if self.cars_speed_counter >= self.cars_slowness:
            for i, car in enumerate(self.traffic):
                self.traffic[i] = offset_sprite(car, offset_x=0, offset_y=1)
            for i, car in enumerate(self.oncoming_traffic):
                self.oncoming_traffic[i] = offset_sprite(car, offset_x=0, offset_y=1)

            self.move_line()
            self.cars_speed_counter = 0

        # oncoming traffic moves 2x faster
        elif self.cars_speed_counter == self.cars_slowness // 2:
            for i, car in enumerate(self.oncoming_traffic):
                self.oncoming_traffic[i] = offset_sprite(car, offset_x=0, offset_y=1)

    def remove_cars(self):
        for car in self.traffic:
            if car[0][1] > MATRIX_HEIGHT:
                self.traffic.remove(car)
        for car in self.oncoming_traffic:
            if car[0][1] > MATRIX_HEIGHT:
                self.oncoming_traffic.remove(car)

    def collision(self):
        for car in (self.traffic + self.oncoming_traffic):
            if intersects(car, self.car):
                self.game_over = True

    def add_points(self):
        for car in (self.traffic + self.oncoming_traffic):
            if check_intersection_x(self.car, car):
                self.score += 10

    def move_line(self):
        if self.line[0][1] >= 3:
            self.line = offset_sprite(self.line, offset_x=0, offset_y=-4)
        else:
            self.line = offset_sprite(self.line, offset_x=0, offset_y=1)

    def main(self):
        if self.game_over:
            return
        self.control()
        self.collision()
        self.add_points()

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_time:
            self.spawn_cars()
            self.spawn_timer = 0

        self.move_cars()
        self.remove_cars()

    def draw(self, screen):
        self.main()
        for pixel in self.car:
            draw_pixel_matrix(screen, pixel)

        for pixel in self.line:
            draw_pixel_matrix(screen, pixel)

        for obstacle in self.traffic + self.oncoming_traffic:
            for pixel in obstacle:
                draw_pixel_matrix(screen, pixel)
