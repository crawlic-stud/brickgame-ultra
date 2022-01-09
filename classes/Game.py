class BaseGame:
    def __init__(self, name):
        self.score = 0
        self.bonus_points = 1000
        self.game_over = False
        self.name = name
        self.speed = 1
        self.level = 1

    def draw(self, *args):
        pass
