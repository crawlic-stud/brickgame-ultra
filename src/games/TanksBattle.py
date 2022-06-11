from src.games.__init__ import *

from src.sprites import TANK, rotate_sprite, convert_with_empty, BORDER, BIG_ROCK, ROCK


class TanksBattle(BaseGame):
    def __init__(self):
        super().__init__('TANKS BATTLE')

        self.tank = Tank((10, 18))

        self.enemies = []
        [self.spawn_enemy(*pos) for pos in SPAWN_POINTS]

        other_obstacles = offset_sprite(BIG_ROCK, 10, 10), offset_sprite(ROCK, 12, 5), offset_sprite(ROCK, 10, 15)
        self.obstacles = [BORDER, *other_obstacles]

        self.shoot_pressed = 0

        self.player_slowness = 21 - self.speed
        self.player_counter = 0

        self.enemy_slowness = self.player_slowness * 3
        self.enemy_counter = 0
        self.enemy_projectile_slowness = 15 - self.speed
        self.enemy_projectile_counter = 0
        self.spawn_counter = 0

        if 0 < self.level < 4:
            self.max_enemies = 2
            self.spawn_delay = 25
            self.max_spawn_distance = 8
        elif 4 < self.level < 7:
            self.max_enemies = 3
            self.spawn_delay = 20
            self.max_spawn_distance = 6
        else:
            self.max_enemies = 4
            self.spawn_delay = 15
            self.max_spawn_distance = 4

    def control(self):
        keys = pygame.key.get_pressed()

        intersections = check_all_intersections(self.tank.sprite, self.obstacles)

        if keys[pygame.K_RIGHT]:
            self.tank.pivot(1)
            if 'right' not in intersections:
                self.move_player(1, 0)
        elif keys[pygame.K_LEFT]:
            self.tank.pivot(3)
            if 'left' not in intersections:
                self.move_player(-1, 0)
        elif keys[pygame.K_UP]:
            self.tank.pivot(0)
            if 'top' not in intersections:
                self.move_player(0, -1)
        elif keys[pygame.K_DOWN]:
            self.tank.pivot(2)
            if 'bottom' not in intersections:
                self.move_player(0, 1)

        if keys[pygame.K_SPACE]:
            if self.shoot_pressed:
                return
            self.tank.shoot()
            self.shoot_pressed += 1
        else:
            self.shoot_pressed = 0

    def move_player(self, dx, dy):
        if self.player_counter % self.player_slowness == 0:
            self.tank.move(dx, dy)
            self.player_counter = 0
        self.player_counter += 1

    def move_projectiles(self):
        self.tank.move_projectile()

        self.enemy_projectile_counter += 1
        if self.enemy_projectile_counter < self.enemy_projectile_slowness:
            return

        for enemy in self.enemies:
            enemy.move_projectile()
        self.enemy_projectile_counter = 0

    def spawn_enemy(self, x, y):
        self.enemies.append(Tank((x, y)))

    def respawn_enemy(self):
        if len(self.enemies) >= self.max_enemies:
            return

        spawn_point = random.choice(SPAWN_POINTS)
        distances = [two_point_distance(spawn_point, (enemy.x, enemy.y)) for enemy in self.enemies] + \
                    [two_point_distance(spawn_point, (self.tank.x, self.tank.y))]

        if min(distances) > self.max_spawn_distance:
            self.spawn_enemy(*spawn_point)

    def move_enemy(self):
        if self.enemy_counter < self.enemy_slowness:
            self.enemy_counter += 1
            return

        for i, enemy in enumerate(self.enemies):

            # only other enemies remain
            enemies = [enemy.get_sprite() for enemy in self.enemies]
            enemies.remove(enemy.get_sprite())

            obstacles = [*enemies, *self.obstacles, self.tank.get_sprite()]

            all_intersections = all_intersections_ai(enemy.get_sprite(), obstacles, 2)

            if not any(all_intersections):
                facing = self.face_towards_player(enemy)
                direction = calculate_direction(facing)
            else:
                direction = calculate_movement(all_intersections)
                facing = calculate_facing(direction)

            if random.randint(0, 1):
                self.enemies[i].shoot()

            self.enemies[i].turn_and_move(direction, facing)

        self.enemy_counter = 0

    def face_towards_player(self, enemy):
        """Should make enemies move towards player"""
        facing = 0

        if enemy.x < self.tank.x and enemy.y < self.tank.y:
            facing = random.choice([1, 2])

        elif enemy.x > self.tank.x and enemy.y > self.tank.y:
            facing = random.choice([0, 3])

        elif enemy.x < self.tank.x:
            facing = 1
        elif enemy.x > self.tank.x:
            facing = 3

        elif enemy.y < self.tank.y:
            facing = 2
        elif enemy.y > self.tank.y:
            facing = 0

        return facing

    def collision(self):
        # check all obstacles in scene
        for i, obstacle in enumerate(self.obstacles):

            # intersection with player projectile and obstacles
            if intersects([self.tank.get_projectile()], obstacle):
                self.obstacles[i].remove(self.tank.get_projectile())
                self.tank.remove_projectile()

            # then check all enemies
            for j, enemy in enumerate(self.enemies):

                # enemy's projectile intersection with obstacles
                if intersects([enemy.get_projectile()], obstacle):
                    self.obstacles[i].remove(enemy.get_projectile())
                    self.enemies[j].remove_projectile()

                # enemy's projectile intersection with player
                if intersects([enemy.get_projectile()], self.tank.get_sprite()):
                    self.tank.sprite = []
                    self.animation.explosion(self.tank.x, self.tank.y)
                    self.game_over = True

                # player intersects with enemy
                if intersects(self.tank.get_sprite(), enemy.get_sprite()):
                    self.tank.sprite = []
                    self.animation.explosion(self.tank.x, self.tank.y)
                    self.game_over = True

                # player's projectile intersection with enemies
                if intersects([self.tank.get_projectile()], enemy.get_sprite()):
                    self.enemies.remove(enemy)
                    self.tank.remove_projectile()
                    self.animation.explosion(enemy.x + 1, enemy.y + 1)
                    ENEMY_DEATH_SOUND.play()
                    self.score += 1000

    def main(self):
        if self.game_over:
            return
        self.control()
        self.collision()
        self.move_projectiles()
        self.move_enemy()

        self.spawn_counter += 1

        if self.spawn_counter > self.spawn_delay:
            self.respawn_enemy()
            self.spawn_counter = 0

    def draw_game(self, screen):
        self.main()

        # for pixel in intersection_circle(self.tank.get_sprite()):
        #     draw_pixel_matrix(screen, pixel)

        for pixel in self.tank.sprite:
            if pixel[2]:
                draw_pixel_matrix(screen, pixel[:-1])

        for enemy in self.enemies:
            for pixel in enemy.sprite:
                if pixel[2]:
                    draw_pixel_matrix(screen, pixel[:-1])
            draw_pixel_matrix(screen, enemy.get_projectile())

        draw_pixel_matrix(screen, self.tank.get_projectile())

        for obstacle in self.obstacles:
            for pixel in obstacle:
                draw_pixel_matrix(screen, pixel)


class Tank:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.sprite = offset_sprite2(convert_with_empty(TANK), self.x, self.y)
        self.facing = 0
        self.projectile = []

    def get_sprite(self):
        return [i[:-1] for i in self.sprite]

    def get_projectile(self):
        return self.projectile[:-2]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def pivot(self, times):
        self.sprite = offset_sprite2(convert_with_empty(rotate_sprite(TANK, times)), self.x, self.y)
        self.facing = times

    def turn_and_move(self, direction, facing):
        self.pivot(facing)
        self.move(*direction)

    def calc_direction(self):
        if self.facing == 0:
            direction = (0, -1)
        elif self.facing == 2:
            direction = (0, 1)
        elif self.facing == 1:
            direction = (1, 0)
        else:
            direction = (-1, 0)
        return direction

    def create_projectile(self):
        direction = self.calc_direction()
        self.projectile = [*self.sprite[4][:-1], *direction]

    def shoot(self):
        # can not shoot if there's already one projectile on the screen
        if self.projectile:
            return

        random.choice([PEW_SOUND_1, PEW_SOUND_2]).play()
        self.create_projectile()

    def remove_projectile(self):
        self.projectile = []

    def move_projectile(self):
        if self.projectile:
            self.projectile[0] += self.projectile[2]
            self.projectile[1] += self.projectile[3]

            if check_border_x([self.get_projectile()]) or check_border_y([self.get_projectile()]):
                self.remove_projectile()
