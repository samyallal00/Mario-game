import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """ Template class for all enemies"""

    def __init__(self, world, initial_dir, image):
        super().__init__()

        # Get to know your world
        self._initialize_world(world)

        # Set up the enemy image
        self._initialize_image(image)

        # set up the positions, x, y, put at same level as mario
        self.rect.y = self.settings.mario_y_pos + 30
        self._initialize_direction(initial_dir)

    def _initialize_world(self, world):
        """ Get to know the world we live in"""
        self.screen = world.screen
        self.settings = world.settings

    def _initialize_image(self, image):
        """ Set up the enemy's image """
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.settings.enemy_width, self.settings.enemy_height))
        self.rect = self.image.get_rect()

    def _initialize_direction(self, initial_dir):
        """ Initialize from where the enemy will pop up """
        self.direction = initial_dir
        if self.direction == 1:
            self.x = self.screen.get_rect().width - 50
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.x = 50

        # Update the real rect value
        self.rect.x = self.x
        self.rect.y = float(self.rect.y)

    def check_edges(self):
        """ Check the edges and revert when reach either edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def revert_direction(self):
        """ Revert direction of the enemy """
        self.direction *= -1

    def update(self):
        """ Update the enemy's movements """
        pass

    def draw_enemy(self):
        """ Draw the enemy image onto the screen """
        self.screen.blit(self.image, self.rect)


class Goomba(Enemy):
    """ Class Goomba derived from enemy """

    def __init__(self, world, initial_dir):
        self.image = pygame.image.load('images/goomba.png')

        super().__init__(world, initial_dir, self.image)

    def update(self):
        """ Update the Goomba's movements """
        self.x += self.settings.goomba_speed * self.direction
        # Update the rect pos
        self.rect.x = self.x


class Troopa(Enemy):
    """ Class Troopa derived from enemy """

    def __init__(self, world, initial_dir):
        self.image = pygame.image.load('images/troopa.png')

        super().__init__(world, initial_dir, self.image)

        # Flags
        self.do_flip = False

    def check_edges(self):
        """ Check the edges and revert when reach either edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            self.do_flip = True
            return True

    def update(self):
        """ Update the Troopa's movements """
        self.x += self.settings.troopa_speed * self.direction

        # Flip the image accordingly, -1 faces to left and 1 to right
        self._position_image()

        # Update the rect pos
        self.rect.x = self.x

    def _position_image(self):
        """ Flip the image accordingly, -1 faces to left and 1 to right """
        if self.direction == -1 and self.do_flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.do_flip = False
        if self.do_flip == 1 and self.do_flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.do_flip = False