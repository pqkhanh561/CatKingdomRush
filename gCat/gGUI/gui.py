import os
import sys
import pygame
from .igame import GameAdapter
from .iloader import ResLoader
from ..gLoader  import ResourceHolder

class GameGUI:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([1200, 1000])

    def _get_game_difficult(self):
        return 0
    
    def _get_game_level(self):
        return 1
    
    def _game_display(self):
        self._show_enemy()
    
    def _display_background(self):
        info, img = ResourceHolder.load_res("sprite_level%d_2-hd" % self._get_game_level())
        background = ResourceHolder.load_image(img, info["frames"]["Stage_%d.png" % (self._get_game_level() + 1)])
        background = pygame.image.fromstring(background.tobytes(), background.size, background.mode).convert_alpha() 
        return background 
        
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.screen.fill((255, 255, 255))
        self.screen.blit(self._display_background(), (0, 0))
        pygame.display.flip()
        self.clock.tick()
        return True
        
    def stop():
        pygame.quit()


if __name__ == '__main__':
    gui = GameGUI()