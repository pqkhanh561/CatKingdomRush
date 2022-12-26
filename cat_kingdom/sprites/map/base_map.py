import pygame
import os
import schedule
import plistlib
from ..monsters.base_monster import *

MonsterType = [Canibal]


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
        self.current_wave = 0
        self.wave_res = []
        self.time = 0
        self.path = None
        self.is_end = False

        self.level = level
        self.difficult = difficult

        self._load_map_resources()
        self.add_monsters_job = schedule.every(1).seconds.do(self._add_monsters_to_wave)

    def _load_background(self):
        info, img = ResourceHolder.load_res("sprite_level%d_2-hd" % self.level)
        background = ResourceHolder.load_image(img, info["frames"]["Stage_%d.png" % (self.level + 1)])
        bg_sprite = pygame.sprite.Sprite()
        bg_sprite.image = background
        bg_sprite.rect = pygame.Rect(0, 0, *background.get_size())
        self.add(bg_sprite)

    def _load_path(self):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_paths.plist" % self.level)
        with open(fname, "rb") as file:
            self.path = plistlib.load(file)['paths']

    def _load_monsters(self):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_%d_monsters.plist" % (self.level, self.difficult))
        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            self.start_gold = int(plist['data'][0]['gold'])
            self.max_life = int(plist['data'][0]['life'])
            self.max_wave = int(plist['data'][0]['wave'])
            self.wave_res = plist['monsters']

    def update(self):
        super(BaseMap, self).update()
        if self.is_end:
            schedule.cancel_job(self.add_monsters_job)

    def _add_monsters_to_wave(self):
        if self.time < len(self.wave_res[self.current_wave]):
            for i in range(len(self.wave_res[self.current_wave][self.time])):
                monster = self.wave_res[self.current_wave][self.time][i]
                try:
                    self.add(MonsterType[int(monster['type'])](self.path[int(monster['road'])][int(monster['path'])]))
                except IndexError:
                    print("Cannot find monster ", int(monster['type']))
                    pass
            self.time += 1
        else:
            self.time = 0
            if self.current_wave != self.max_wave - 1:
                self.current_wave += 1
            else:
                self.is_end = True
                return

    def _load_map_resources(self):
        self._load_monsters()
        self._load_path()
        self._load_background()
