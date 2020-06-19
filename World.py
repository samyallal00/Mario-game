import pygame
import sys
import random
from time import sleep

from settings import Settings
from player import Player
from bullet import Bullet
from enemies import Enemy, Goomba, Troopa
from game_stats import Stats


class World:
    """ Main world that keeps track of everything """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Set up the settings of the game
        self.settings = Settings(self)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Create the game stats object
        self.stats = Stats(self)

        # Create the Mario instance, and bullets, and enemies
        self.mario = Player(self)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def run_game(self):
        """ Main loop """

        while True:
            self._check_events()
            self.mario.update()
            self._update_bullets()
            self._update_enemies()
            self._update_screen()

    def _check_events(self):
        """ Check the keyboard and mouse presses """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                self._check_keydowns(event)
            elif event.type == pygame.KEYUP:
                self._check_keyups(event)

    def _check_keydowns(self, event):
        """ Check when the keys are pressed"""
        if event.key == pygame.K_q:
            sys.exit(0)
        elif event.key == pygame.K_UP:
            if not self.mario.is_currently_jumping:
                self.mario.jumping = self.settings.mario_jump_max
        elif event.key == pygame.K_RIGHT:
            self.mario.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.mario.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet(self.settings.direction)

    def _check_keyups(self, event):
        """ Check when the keys are released"""
        if event.key == pygame.K_UP:
            if self.mario.jumping <= 0:
                self.mario.jumping = 0
        elif event.key == pygame.K_RIGHT:
            self.mario.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.mario.moving_left = False

    def _fire_bullet(self, initial_dir):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.max_num_bullets:
            new_bullet = Bullet(self, initial_dir)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update the bullets positions """
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.direction == 1 and bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
            elif bullet.direction == -1 and bullet.rect.right <= 0:
                self.bullets.remove(bullet)

    def _create_enemy(self, enemy_type):
        """ Create an enemy in the game with a random direction """
        rand = random.choice([-1, 1])
        new_enemy = 0
        if enemy_type == 1:
            new_enemy = Goomba(self, rand)
        if enemy_type == 2:
            new_enemy = Troopa(self, rand)
        self.enemies.add(new_enemy)

    def _popup_enemy(self):
        """ Pop up enemies during the game at random times """
        rand = random.choice(range(100))
        if rand == 1 and self.stats.goomba_active <= self.settings.enemy_num_max:
            self._create_enemy(1)
            self.stats.goomba_active += 1
        if rand == 2 and self.stats.troopa_active <= self.settings.enemy_num_max:
            self._create_enemy(2)
            self.stats.troopa_active += 1

    def _revert_enemies_edges(self):
        """ Revert enemies directions when they hit edges """
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                enemy.revert_direction()

    def _check_bullet_enemy_collision(self):
        """ Kill any hit goombas """
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        # Update the number of enemies in stats accordingly
        if collisions:
            for enemies in collisions.values():
                if isinstance(enemies, Goomba):
                    self.stats.goomba_active -= 1
                if isinstance(enemies, Troopa):
                    self.stats.troopa_active -= 1

    def _update_enemies(self):
        """ Update the group of enemies movements and behaviors """
        self._popup_enemy()
        self._revert_enemies_edges()
        self._check_bullet_enemy_collision()
        self.enemies.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.mario, self.enemies):
            self._mario_hit()

    def _mario_hit(self):
        """ Kill Mario when hit by an ennemy """
        self.stats.mario_lives_left -= 1

        # Reset everything
        self.enemies.empty()
        self.bullets.empty()
        self.mario.center_mario()

        sleep(1)

    def _update_screen(self):
        """ Update the overall screen components """
        self.screen.fill(self.settings.screen_color)
        self.settings.set_up_backgroud()

        self.mario.blitme()
        # Draw the bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw enemies on the screen
        for enemy in self.enemies.sprites():
            enemy.draw_enemy()

        pygame.display.flip()


if __name__ == '__main__':
    game = World()
    game.run_game()
