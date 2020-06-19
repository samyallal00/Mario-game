class Stats:
    """ Keeps track of the game's stats """

    def __init__(self, world):
        self.screen = world.screen
        self.settings = world.settings

        self.mario_lives_left = self.settings.mario_lives_max

        self.goomba_active = 0
        self.troopa_active = 0
