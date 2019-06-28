#!/usr/bin/env python
from animationLib import *
from objects import * 

class Game(Animation):
    def __init__(self, dimensions, width, height, fps=30, background="black"):
        super().__init__(width, height, fps, background, refresh_bg=False)
        
        self.ball = Ball(1, self.colours["red"], [0, height/2])
        
        self.ball.aVelocity = 0.2
        self.amplitude  = 100
        
    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def game_logic(self):
        x = self.amplitude * sin(self.ball.angle)
        x = map_range(x, -300, 300, 0, 600)
        self.ball.pos[0] = x

        y = self.amplitude * cos(self.ball.angle)
        y = map_range(y, -300, 300, 0, 600)
        self.ball.pos[1] = y * random.uniform(0,1) 

        self.ball.update()

    def display_logic(self):    
        #self.ball.draw_line(self.screen)
        self.ball.draw(self.screen)

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

