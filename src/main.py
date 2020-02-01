#!/usr/bin/env python
from animationLib import *
from objects import * 
from constants import *


class Game(Animation):
    def __init__(self, dimensions, width, height, fps=30, background=BLACK):
        super().__init__(width, height, fps, background)
        
    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()

    def game_logic(self):
        pass

    def display_logic(self):    
        pass

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

