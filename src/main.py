#!/usr/bin/env python
from animationLib import *
from objects import * 
from constants import *
from math import sin, cos, pi
import pygame


# TODO:
#       Make wave "bounce" off surface instead of 
#           using 2 waves.


class Game(Animation):
    def __init__(self, dimensions, width, height, fps=80, background=BLACK):
        super().__init__(width, height, fps, background)
        self.move = 0
        self.points = []
        self.wave  = Wave(30, self.width, self.height)
        self.wave2 = Wave(30, self.width, self.height)
        self.wave3 = Wave(30, self.width, self.height)

    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(self.wave.points) 
            print(self.wave2.points) 
            print(self.wave3.points) 

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()

    def game_logic(self):
        self.wave.oscillate(self.height / 2, scaling_time=self.fps)
        self.wave2.oscillate(self.height / 2, flip=-1, scaling_time=self.fps)
    
        # only works if both waves have same number of points 
        self.wave3.points = [(self.wave.points[i][0], self.wave.points[i][1] + self.wave2.points[i][1] - int(self.height / 2)) for i in range(len(self.wave.points))] 

    def display_logic(self):    
        self.wave.draw(self.screen)
        self.wave2.draw(self.screen)
        self.wave3.draw(self.screen, line_col=CYAN, point_col=MAGENTA)

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

