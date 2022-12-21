from PIL import Image
import matplotlib.pyplot as plt
import os
import sys
import schedule
import pygame
from .utils.res import ResourceHolder
from .sprites.monsters.base_monster import Canibal
from .sprites.map.base_map import BaseMap


def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([960, 640])
    running = True
    map = BaseMap()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        map.update()
        map.draw(screen)
        # pygame.display.update()
        pygame.display.flip()
        schedule.run_pending()
        clock.tick()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(run())
