#!/usr/bin/env python
from animationLib import *
from random import randint
from math import *
import numpy as np

def get_sign(number):
    return -1 if number < 0 else 1

class Ball():
    def __init__(self, radius, colour, pos, weight=10, gravity=9.81):
        self.radius      = radius
        self.colour      = colour
        self.pos         = np.asarray(pos)

        self.velocity       = np.asarray((0, 0), dtype=int)
        self.acceleration   = np.asarray((0, 0), dtype=int) 
        

class Game(Animation):
    def __init__(self, x, y, width, height, fps=30, background="black", gravity=9.81):
        super().__init__(width, height, fps, background)
        
        self.ball = Ball(10, self.colours["red"], (x,y))
    
    def game_logic(self):
        mouse = np.asarray(pygame.mouse.get_pos())
        diff  = np.subtract(mouse, self.ball.pos)

        self.ball.acceleration  = np.multiply(diff, 0.01)
        self.ball.velocity      = np.add(self.ball.velocity, self.ball.acceleration)
        self.ball.pos           = np.add(self.ball.pos, self.ball.velocity)

    def display_logic(self):
        pygame.draw.circle(self.screen, self.ball.colour, np.round(self.ball.pos).astype(int), self.ball.radius)


def main():
    width, height = 900, 900 
    game = Game(randint(40, width-40), randint(40, height-40), width, height)
    game.main()

if __name__ == "__main__":
    main()

