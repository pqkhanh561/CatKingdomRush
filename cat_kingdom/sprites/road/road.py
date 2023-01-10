import os
import plistlib

import pygame

from cat_kingdom.sprites.monsters.base_monster import Canibal
from cat_kingdom.utils.res import ResourceHolder

MonsterType = [Canibal]


class Road(pygame.sprite.Group):
    def __init__(self, level, difficult):
        super(Road, self).__init__()
        self.time = 0
        self.terrians = []
        self.enemies = []
        self.path = []
        self.gold_update_func = None
        self.current_wave = 0

        self._load_map_resources(level, difficult)

    def _load_map_resources(self, level, difficult):
        self._load_monsters(level, difficult)
        self._load_path(level)
        self._load_background(level)

    def update_components(self):
        """ Check the life of the game and update gold and life"""
        pass

    def _load_background(self, level):
        info, img = ResourceHolder.load_res("sprite_level%d_2-hd" % level)
        background = ResourceHolder.load_image(img, info["frames"]["Stage_%d.png" % (level + 1)])
        bg_sprite = pygame.sprite.Sprite()
        bg_sprite.image = background
        bg_sprite.rect = pygame.Rect(0, 0, *background.get_size())
        self.add(bg_sprite)

    def _load_path(self, level):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_paths.plist" % level)
        with open(fname, "rb") as file:
            self.path = plistlib.load(file)['paths']

    def _load_monsters(self, level, difficult):
        fname = os.path.join(os.getenv("RESOURCE_PATH"), "level%d_%d_monsters.plist" % (level, difficult))
        with open(fname, "rb") as file:
            plist = plistlib.load(file)
            self.start_gold = int(plist['data'][0]['gold'])
            self.max_life = int(plist['data'][0]['life'])
            self.max_wave = int(plist['data'][0]['wave'])
            self.wave_res = plist['monsters']

    def create_monster(self):
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
