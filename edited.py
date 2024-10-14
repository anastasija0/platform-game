import pygame
import math
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCREEN_SIZE)
        self.bg = pygame.image.load('BG.png')
        pygame.display.set_caption('igrica')
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data=[]
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
              self.map_data.append(line)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets=pygame.sprite.Group()
        self.enemies=pygame.sprite.Group()
            
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(30)
            self.events()
            self.update()
            self.draw()
            
    def quit(self):
        pygame.quit()
        sys.exit()
        
    def update(self):
        self.all_sprites.update()
    def draw(self):
        self.screen.blit(self.bg,(0,0))
        self.all_sprites.draw(self.screen)
        pygame.display.update()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.key == pygame.K_ESCAPE:
                self.quit()
            #...
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
    
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
        
    
