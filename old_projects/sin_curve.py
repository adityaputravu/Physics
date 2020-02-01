#!/usr/bin/env python
from animationLib import *
from objects import * 
from constants import *
from math import sin, cos, pi
from random import choice 
import time

class Game(Animation):
    def __init__(self, dimensions, width, height, fps=20, background=BLACK):
        super().__init__(width, height, fps, background)
        self.move = 0
        self.points = []

    def f(self, x, wavelength, amplitude, oscillations=2):
        return int( (sin((oscillations * 2 * pi * -x) / wavelength) * amplitude + amplitude) / 2 ) 

    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(self.mult) 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()

    def game_logic(self):
        self.move = pygame.time.get_ticks() / 4000
        self.points = [(x, self.f(x - (self.move * self.width), self.width, self.height)) for x in range(self.width)]

    def display_logic(self):    
        pygame.draw.line(self.screen, WHITE, (0, self.height / 2), (self.width, self.height / 2))
        # pygame.draw.lines(self.screen, BLUE, False, self.points[:int(len(self.points) / 2)]) 
        # pygame.draw.lines(self.screen, RED, False, self.points[int(len(self.points) / 2):]) 
        pygame.draw.lines(self.screen, RED, False, self.points, 5)

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

