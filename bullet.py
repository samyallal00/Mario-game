import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Main class for the bullet """

    def __init__(self, world, initial_dir):
        super().__init__()

        # Get info about the world in the game
        self.world = world
        self.screen = world.screen
        self.settings = world.settings
        self.direction = initial_dir

        # Set up the image of the bullet and resize
        self.image = pygame.image.load('images/Fireball-PNG-HD-Image.png')
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        self.rect = self.image.get_rect()

        # Start with the bullet at the right of mario
        self._set_starting_point()
        self.up_down_ratio = 0

        self.x, self.y = float(self.rect.x), float(self.rect.y)

    def _set_starting_point(self):
        """ Set the starting point of a bullet """
        if self.direction == 1:
            self.rect.midleft = self.world.mario.rect.midright
        else:
            self.rect.midright = self.world.mario.rect.midleft

    def update(self):
        """ Update the behavior of bullet """
        self._update_x_pos()
        self._update_y_pos()

        # Increment the ratio for a wave effect, and flip
        self.image = pygame.transform.flip(self.image, True, False)
        self.up_down_ratio += 1

    def _update_x_pos(self):
        """ Update the x position of the bullet"""
        self.x += self.settings.bullet_speed * self.direction
        self.rect.x = self.x

    def _update_y_pos(self):
        """ Update the y position of the bullet"""
        if self.up_down_ratio % 2 == 0:
            self.y += 10
        else:
            self.y -= 10
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet on screen """
        self.screen.blit(self.image, self.rect)
