import pygame


class Player:
    """ Define the player here """

    def __init__(self, world):
        # Need to have access to the world he is living in
        self.screen = world.screen
        self.settings = world.settings
        self.screen_rect = self.screen.get_rect()

        # set up the image for mario
        self.image = pygame.image.load('images/mario_PNG8.bmp')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        # set up initial pos of mario in the middle of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 150
        self.settings.mario_y_pos = self.rect.y

        # set up the x, y coordinates
        self.x, self.y = float(self.rect.x), float(self.rect.y)

        # Movement flag self.
        self.moving_right = self.moving_left = self.is_currently_jumping = False
        self.jumping = 0

    def center_mario(self):
        """ Center Mario everytime the game ends or player loses """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x, self.y = float(self.rect.x), float(self.rect.y)

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the mario's x, y values, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self._move_right()
        if self.moving_left and self.rect.left > 0:
            self._move_left()
        if self.jumping > 0:
            self._perform_jump()
        if self.jumping <= 0:
            self._perform_landing()

        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

    def _perform_jump(self):
        """ Perform the jump """
        # by decreasing the y, going up on each iteration and setting the flags properly
        self.y -= self.settings.mario_jump_speed
        self.jumping -= self.settings.mario_jump_speed
        self.is_currently_jumping = True

    def _perform_landing(self):
        """ Perform the landing after the jump """
        self.y += self.settings.mario_jump_speed
        if self.y >= self.settings.mario_y_pos:
            self.y = self.settings.mario_y_pos
            self.jumping = 0
            self.is_currently_jumping = False

    def _move_right(self):
        """ Moves the player right """
        self.x += self.settings.mario_speed
        if self.settings.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.settings.direction = 1

    def _move_left(self):
        """ Moves the player left """
        self.x -= self.settings.mario_speed
        if self.settings.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.settings.direction = -1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)