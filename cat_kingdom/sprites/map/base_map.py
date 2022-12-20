import pygame
import os
import plistlib
from ..monsters.base_monster import *

MonsterType = [Canibal]


class BaseMap(pygame.sprite.Group):
    def __init__(self, screen):
        super(BaseMap, self).__init__()
        self.level = 0
        self.difficult = 0
        self.start_gold = 0
        self.max_life = 0
        self.max_wave = 0
        self.current_wave = 0
        self.wave_res = []
        self.time = 0
        self.path = None
        self.screen = screen
        self._load_resource()
        self._load_path()
        self._add_monsters_to_wave()

    def _load_path(self):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_paths.plist" % (self.level))
        with open(fname, "rb") as file:
            self.path = plistlib.load(file)['paths']

    def _load_resource(self):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_%d_monsters.plist" % (self.level, self.difficult))
        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            self.start_gold = int(plist['data'][0]['gold'])
            self.max_life = int(plist['data'][0]['life'])
            self.max_wave = int(plist['data'][0]['wave'])
            self.wave_res = plist['monsters']

    def _add_monsters_to_wave(self):
        if self.time < len(self.wave_res[self.current_wave]):
            for i in range(len(self.wave_res[self.current_wave][self.time])):
                monster = self.wave_res[self.current_wave][self.time][i]
                self.add(MonsterType[int(monster['type'])](self.screen, self.path[self.current_wave][self.time]))
            self.time += 1




