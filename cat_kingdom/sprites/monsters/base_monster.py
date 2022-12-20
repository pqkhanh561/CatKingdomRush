from enum import Enum
import pygame
import os
import json
from cat_kingdom.utils.res import ResourceHolder
import random
import math


class TypeMonster(Enum):
    CANIBAL = 0


class State(Enum):
    IDLE = 0
    RUN = 1
    ATTACK = 2
    DEATH = 4
    FINISH = 5


class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, screen, path):
        super(BaseMonster, self).__init__()
        self.name = None
        self.action = None
        self.state = State.IDLE
        self.screen = screen
        self.rect = None
        self.current_action = "left"
        self.action_idx = 0
        self.pos = [0, 0]
        self.path = path
        self.next_point_idx = 0
        self.last_update_action = 0
        self.state = State.RUN

    def set_delay(self, delay):
        self.delay = delay

    def _load_animation(self):
        info, img = ResourceHolder.load_res("enemies_jungle-hd")
        sprite_dict = {k: v for k, v in info['frames'].items() if self.name + "_" in k}
        for k, v in sprite_dict.copy().items():
            aliases = v["aliases"]
            for alias in aliases:
                sprite_dict.update({alias: v.copy()})
                sprite_dict[alias].pop("aliases")
            sprite_dict[k].pop("aliases")

        sprite_info = None
        with open(os.path.join(os.getenv("RESOURCE_PATH"), "object_sprite.json")) as f:
            sprite_info = json.load(f)[self.name]

        action = "runleft"
        self.set_delay(float(sprite_info[action]["delay"]))
        left_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                       sprite_info[action]["prefix"],
                                                       sprite_info[action]["start"],
                                                       sprite_info[action]["end"],
                                                       True)
        action = "runright"
        right_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                        sprite_info[action]["prefix"],
                                                        sprite_info[action]["start"],
                                                        sprite_info[action]["end"])
        action = "runup"
        up_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                     sprite_info[action]["prefix"],
                                                     sprite_info[action]["start"],
                                                     sprite_info[action]["end"])
        action = "rundown"
        down_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                       sprite_info[action]["prefix"],
                                                       sprite_info[action]["start"],
                                                       sprite_info[action]["end"])
        action = "death"
        death_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                        sprite_info[action]["prefix"],
                                                        sprite_info[action]["start"],
                                                        sprite_info[action]["end"])
        action = "attack"
        attack_seq = ResourceHolder.load_images_sequence(sprite_dict, img,
                                                         sprite_info[action]["prefix"],
                                                         sprite_info[action]["start"],
                                                         sprite_info[action]["end"])
        self.action = {
            "left": left_seq,
            "right": right_seq,
            "up": up_seq,
            "down": down_seq,
            "death": death_seq,
            "attack": attack_seq
        }

    def _get_next_point(self):
        return float(self.path[self.next_point_idx]['x']), float(self.path[self.next_point_idx]['y'])

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
            self.next_point_idx += 1
            if self.next_point_idx > len(self.path[self.next_point_idx]):
                self.state = State.FINISH
            if self.state == State.RUN:
                self.action_idx += 1
                if self.action_idx > len(self.action[self.current_action]) - 1:
                    self.action_idx = 0
                # getattr(self, self.current_action)()
                self.image = self.action[self.current_action][self.action_idx]
                self.rect = pygame.Rect(*self._get_next_point(), *self.image.get_size())

class Canibal(BaseMonster):
    def __init__(self, screen, path):
        super(Canibal, self).__init__(screen, path)
        print("Create Canibal")
        self.name = "Canibal"
        self._load_animation()
        # self.image = self.action[self.current_action][self.action_idx]
        # self.pos = list(self._get_next_point())
        # self.rect = pygame.Rect(*self.pos, *self.image.get_size())
        self.next_point_idx += 1

    def __str__(self):
        return "Canibal"
