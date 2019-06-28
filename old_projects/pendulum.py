#!/usr/bin/env python
from animationLib import *
from objects import Rect 

class Game(Animation):
    def __init__(self, dimensions, width, height, fps=30, background="black"):
        super().__init__(width, height, fps, background)
        
        self.aVel = 0
        self.aAcc = 0.01

        self.r = 150
        self.a = pi/4
        self.pos = (width/2, height/2)
        self.starting_pos = self.pos
        
    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def game_logic(self):
        x = self.r * sin(self.a)
        y = self.r * cos(self.a)
        self.pos = np.add(self.starting_pos, (x, y)).astype(int)
        
        dist = pygame.mouse.get_pos()
        dist = sqrt(pow(dist[0], 2) + pow(dist[1], 2))
        self.aAcc = map_range(dist, 300, 700, -0.01, 0.01)
        self.a += self.aVel
        self.aVel += self.aAcc
         

        print(f"Pos: {self.pos}\naVel: {self.aVel}\n, dist: {dist}\naAcc: {self.aAcc}\n")

    def display_logic(self):    
        pygame.draw.line(self.screen, self.colours["white"], self.starting_pos, self.pos)
        pygame.draw.circle(self.screen, self.colours["red"], self.pos, 10)

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

