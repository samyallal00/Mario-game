import pygame


class Settings:
    """ Control the settings of the game """

    def __init__(self, world):
        # World settings
        self.world = world
        self.screen_width = 1200
        self.screen_height = 800
        self.screen_color = (230, 230, 230)

        # Mario Settings
        self.mario_speed = 20.5
        self.mario_lives_max = 5
        self.mario_jump_max = 180
        self.mario_jump_speed = 20.5
        self.mario_y_pos = 0

        # Bullets settings
        self.bullet_speed = 12.0
        self.bullet_width = 30
        self.bullet_height = 30
        self.max_num_bullets = 5

        # Direction of Both Bullet and Mario, 1 is right, -1 left
        self.direction = 1

        # Enemy settings
        self.enemy_width = 45
        self.enemy_height = 45
        self.goomba_speed = 3.5
        self.troopa_speed = 5.5
        self.enemy_num_max = 5

    def set_up_backgroud(self):
        self.image = pygame.image.load('images/mario-bg.jpg')
        self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        self.rect = self.image.get_rect()

        self.world.screen.blit(self.image, self.rect)

