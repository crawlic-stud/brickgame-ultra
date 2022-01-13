class Settings:
    def __init__(self, game):
        self.game = game

    # TODO: create all buttons and configure them

    def show(self):
        self.game.pause()
        # TODO: show settings

    def close(self):
        self.game.unpause()
        # TODO close settings and continue with new params

    # TODO: implement all switch functions
    def switch_something(self):
        pass
