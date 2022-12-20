from PIL import Image
import matplotlib.pyplot as plt
import os
import sys
import pygame
from .utils.res import ResourceHolder
from .sprites.monsters.base_monster import Canibal
from .sprites.map.base_map import BaseMap

os.environ["RESOURCE_PATH"] = "./Resources"

def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1200, 1200])
    running = True
    map = BaseMap(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        map.update()
        map.draw(screen)
        pygame.display.update()
        clock.tick()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(run())
