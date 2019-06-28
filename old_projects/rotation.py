#!/usr/bin/env python
from animationLib import *
from objects import Rect 

class Game(Animation):
    def __init__(self, dimensions, width, height, fps=30, background="black"):
        super().__init__(width, height, fps, background)
        
        x,y,rect_width,rect_height = dimensions
        self.rect = Rect(x, y, rect_width, rect_height, self.colours["red"])
        self.midpoint = (x + rect_width/2, y + rect_height/2)

        self.a      = 0
        self.aVel   = 0  
        self.aAccel = 0.01

    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def game_logic(self):
        
        self.rect.update()
        self.a += self.aVel
        self.aVel += self.aAccel
        self.rect.rotate_clockwise(self.a, r_point=self.rect.find_centroid())

    def display_logic(self):    
        self.rect.draw(self.screen)
        
        # Centre dot
        pygame.draw.circle(self.screen, self.colours["blue"], (round(self.width/2), round(self.height/2)), 1)

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

