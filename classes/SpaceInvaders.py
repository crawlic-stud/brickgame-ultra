from classes.__init__ import *
from sprites import ENEMIES_SMALL, ENEMIES_BIG, \
    SHIP_1, SHIP_2, SHIP_3, \
    PROJECTILE_1, PROJECTILE_2, PROJECTILE_3


class SpaceInvaders(BaseGame):
    def __init__(self):
        super().__init__('SPACE INVADERS')
        self.ship = sprite_to_bottom(SHIP_3)
        self.ship_slowness = 2
        self.ship_speed_counter = 0
        self.enemy_slowness = 30
        self.enemy_speed_counter = 0
        self.shoot_delay = 0
        self.enemies = []
        self.spawn_enemy(random.choice(ENEMIES_SMALL), offset_y=0, offset_x=MATRIX_WIDTH//3)
        self.projectiles = []
        self.enemy_projectiles = []
        play_music(SECOND_THEME)

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and check_border_x(self.ship) != 'right':
            self.move_player(1, 0)
        elif keys[pygame.K_LEFT] and check_border_x(self.ship) != 'left':
            self.move_player(-1, 0)
        elif keys[pygame.K_UP] and check_border_y(self.ship) != 'top':
            self.move_player(0, -1)
        elif keys[pygame.K_DOWN] and check_border_y(self.ship) != 'bottom':
            self.move_player(0, 1)

        self.ship_speed_counter += 1

        if keys[pygame.K_SPACE]:
            self.shoot()
            self.shoot_delay += 1
            if self.shoot_delay > 100:
                self.shoot_delay -= 50
        else:
            self.shoot_delay = 0

    def move_player(self, dx, dy):
        if self.ship_speed_counter % self.ship_slowness == 0:
            new_ship = [[pixel[0] + dx, pixel[1] + dy] for pixel in self.ship]
            self.ship = new_ship
            self.ship_speed_counter = 0

    def move_enemy(self):
        self.enemy_speed_counter += 1
        if self.enemy_speed_counter < self.enemy_slowness:
            return

        for i, enemy in enumerate(self.enemies):

            # if enemy ship reached bottom - game over
            if check_border_y(enemy) == 'bottom':
                self.game_over = True
                # self.enemies.remove(self.enemies[i])
                continue

            vel_y = 1

            # if there is no other enemy ships - then it's boss
            if check_border_x(enemy) == 'right':
                vel_x = random.randint(-1, 0)
            elif check_border_x(enemy) == 'left':
                vel_x = random.randint(0, 1)
            else:
                vel_x = random.randint(-1, 1)

            if check_intersection_y(enemy, [[i, MAX_ROW] for i in range(MATRIX_WIDTH)]):
                vel_y = 0

            others = self.enemies[:i] + self.enemies[i + 1:]
            for other in others:

                # avoid intersections with other enemy ships on x axis
                if check_border_x(enemy) != 'right' and check_intersection_x(enemy, other) == 'right':
                    vel_x = 1
                elif check_border_x(enemy) != 'left' and check_intersection_x(enemy, other) == 'left':
                    vel_x = -1

                # if not near other ship - then move randomly left to right
                else:
                    if check_border_x(enemy) != 'left' and check_border_x(enemy) != 'right':
                        vel_x = random.randint(-1, 1)
                    elif check_border_x(enemy) == 'left':
                        vel_x = random.randint(0, 1)
                    elif check_border_x(enemy) == 'right':
                        vel_x = random.randint(-1, 0)

                # avoid intersections with other ships on y axis
                if check_border_x(enemy) != 'bottom' and check_intersection_y(enemy, other) == 'bottom':
                    vel_y = -1
                elif check_border_x(enemy) != 'top' and check_intersection_y(enemy, other) == 'top':
                    vel_y = 1

                # if nothing interferes - keep going downwards
                else:
                    vel_y = 1

            self.enemies[i] = [[pixel[0] + vel_x, pixel[1] + vel_y] for pixel in enemy]
            self.enemy_speed_counter = 0

    def shoot(self):
        if self.shoot_delay % (len(self.ship) * 3) == 0:
            random.choice([PEW_SOUND_1, PEW_SOUND_2]).play()
            offset_x = self.ship[0][0]
            offset_y = self.ship[0][1]

            if len(self.ship) == 4:
                self.projectiles += [[i[0] + offset_x, i[1] + offset_y] for i in PROJECTILE_1]
            elif len(self.ship) == 7:
                self.projectiles += [[i[0] + offset_x, i[1] + offset_y] for i in PROJECTILE_2]
            else:
                self.projectiles += [[i[0] + offset_x, i[1] + offset_y] for i in PROJECTILE_3]

    def enemy_shoot(self):
        pass

    def move_projectiles(self):
        new_projectiles = []
        for i, projectile in enumerate(self.projectiles):
            if projectile[1] < 0:
                continue
            new_projectiles.append([projectile[0], projectile[1] - 1])
        self.projectiles = new_projectiles

    def collision(self):
        for i, enemy in enumerate(self.enemies):

            if intersects(self.ship, enemy):
                self.game_over = True

            intersection = intersects(self.projectiles, enemy)
            if not intersection:
                self.bonus_points = 100
                continue
            for point in intersection:
                self.score += self.bonus_points
                self.bonus_points += 100
                self.projectiles.remove(point)
                self.enemies[i].remove(point)

    def spawn_enemy(self, enemy, offset_x=random.choice([0, 6, 12]), offset_y=random.randint(10, 20)):
        enemy = [[pos[0] + offset_x, pos[1] - offset_y] for pos in enemy]
        self.enemies.append(enemy)

    def spawn_wave(self, wave=ENEMIES_SMALL):
        self.spawn_enemy(random.choice(wave), offset_x=0)
        # self.spawn_enemy(random.choice(wave), offset_x=MATRIX_WIDTH // 3)
        self.spawn_enemy(random.choice(wave), offset_x=2 * MATRIX_WIDTH // 3)

    def main(self):
        if self.game_over:
            return

        if len(self.enemies) < 3:
            if random.randint(0, 5):
                self.spawn_wave(ENEMIES_SMALL)
            else:
                self.spawn_enemy(random.choice(ENEMIES_BIG), offset_x=5, offset_y=30)
            # self.spawn_wave([ENEMY_BIG_1, ENEMY_BIG_2])

        for enemy in self.enemies:
            if len(enemy) < 4:
                ENEMY_DEATH_SOUND.play()
                self.enemies.remove(enemy)

        self.control()
        self.move_enemy()
        self.move_projectiles()
        self.collision()

    def draw(self, screen):
        self.main()

        for pixel in self.ship:
            draw_pixel_matrix(screen, pixel)

        for pixel in self.projectiles:
            draw_pixel_matrix(screen, pixel)

        for enemy in self.enemies:
            for pixel in enemy:
                draw_pixel_matrix(screen, pixel)
