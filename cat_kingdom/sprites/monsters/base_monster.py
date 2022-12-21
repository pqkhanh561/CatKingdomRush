import json
import os
from enum import Enum

import pygame

from cat_kingdom.utils.res import ResourceHolder


class TypeMonster(Enum):
    CANIBAL = 0


class State(Enum):
    IDLE = 0
    RUN = 1
    ATTACK = 2
    DEATH = 4
    FINISH = 5
    REMOVING = 6


class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, path):
        super(BaseMonster, self).__init__()
        self.delay = None
        self.path = path
        self.name = None
        self.action = None
        self.state = State.IDLE
        self.rect = None
        self.current_action = "left"
        self.action_idx = 0
        self.pos = [0, 0]
        self.next_point_idx = 0
        self.last_update_action = 0
        self.state = State.RUN

    def set_delay(self, delay):
        self.delay = delay

    def _load_animation(self):
        self.action = ResourceHolder().get_enemy(self.name)
        self.delay = self.action['delay']

    def _get_next_point(self):
        return float(self.path[self.next_point_idx]['x']), \
               float(self.path[self.next_point_idx]['y'])

    def death(self):
        self.current_action = "death"

    def attach(self):
        self.current_action = "attack"

    def up(self):
        self.current_action = "up"

    def down(self):
        self.current_action = "down"

    def left(self):
        self.current_action = "left"

    def right(self):
        self.current_action = "right"
        self.pos[0] = self.pos[0] + 1
        self.rect = pygame.Rect(*self.pos, *self.image.get_size())

    def update(self):
        if pygame.time.get_ticks() - self.last_update_action > self.delay * 1000:
            self.last_update_action = pygame.time.get_ticks()

            if self.state == State.RUN:
                self.next_point_idx += 1
                if self.next_point_idx >= len(self.path) - 1:
                    self.state = State.FINISH
                self.action_idx += 1
                if self.action_idx > len(self.action[self.current_action]) - 1:
                    self.action_idx = 0
                # getattr(self, self.current_action)()
                self.image = self.action[self.current_action][self.action_idx]
                self.rect = pygame.Rect(*self._get_next_point(), *self.image.get_size())
            if self.state == State.FINISH:
                self.kill()
            if self.state == State.REMOVING:
                self.kill()

    def remove_monster(self):
        self.state = State.REMOVING


class Canibal(BaseMonster):
    def __init__(self, path):
        super(Canibal, self).__init__(path)
        self.name = "Canibal"
        self._load_animation()

    def __str__(self):
        return self.name
