import pygame
import os
import schedule
import plistlib
from ..monsters.base_monster import *
from ..road.road import Road


class BaseMapMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseMap(pygame.sprite.Group, metaclass=BaseMapMeta):
    def __init__(self, level, difficult):
        super(BaseMap, self).__init__()
        self.start_gold = 0
        self.max_life = 0
        self.max_wave = 0

        self.wave_res = []
        self.time = 0
        self.is_end = False

        self.level = level
        self.difficult = difficult

        self.add_monsters_job = schedule.every(1).seconds.do(self._add_monsters_to_wave)

        self.road = Road(level, difficult)
        self.add(self.road)

        self.add_monsters_job.run()

    def update(self):
        super(BaseMap, self).update()
        if self.is_end:
            schedule.cancel_job(self.add_monsters_job)
        self.road.draw()

    def _add_monsters_to_wave(self):
        self.road.create_monster()
