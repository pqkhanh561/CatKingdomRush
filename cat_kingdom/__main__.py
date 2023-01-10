import os
import sys
import schedule
import pygame
from .sprites.map.base_map import BaseMap


def run():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1200, 1000])
    running = True
    game_map = BaseMap(1, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        game_map.update()
        game_map.draw(screen)
        # pygame.display.update()
        pygame.display.flip()
        schedule.run_pending()
        clock.tick()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(run())
