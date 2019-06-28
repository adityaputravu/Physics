#!/usr/bin/env python
from animationLib import *
from objects import Rect 
from random import randint, uniform, choice

class Game(Animation):
    def __init__(self, number, x_range, y_range, width, height, fps=30, background="black", gravity=9.81):
        super().__init__(width, height, fps, background)
        
        allowed_colours = list(self.colours.keys())
        allowed_colours.remove('black')

        distance = randint(0,50)
        self.balls = [ 
                        Rect(
                               randint(50, self.width-50),
                               randint(50, self.height-50),
                               distance,
                               distance,
                               self.colours["red"],
                               id=i
                            ) 
                                          
                      
                      for i in range(number)]

        self.centre_ball = Rect(self.width/2, self.height/2, 50,50, self.colours["blue"])
    
    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(f"{pygame.mouse.get_pos()},")
            pygame.draw.circle(self.screen, self.colours['white'], pygame.mouse.get_pos(), 4)
            for ball in self.balls:
                ball.apply_force([4,2])

    def game_logic(self):
        selected = None 
        moving   = False
        gravity = [0, 3]
        for ball in self.balls:
            #ball.apply_gravity(gravity)
            #ball.apply_fluid_resistance(1, 0.0001)
            ball.apply_force([0.1,0]) 

            force = ball.apply_gravitation_attraction(2, self.centre_ball.mass, self.centre_ball.find_centroid())
            self.centre_ball.apply_gravitation_attraction(0.0001, ball.mass, ball.find_centroid())

            #if ball.pos[1] == self.height - ball.radius:
            #    ball.apply_friction(0.1, gravity)
            

            #print(f"Ball: {ball.id}\nArea: {ball.find_area()}\nReal area: {ball.area}\npoints: {ball.points}\n")
            ball.update()
             
            #self.centre_ball.update()
            #trimmed                 = trim([0+ball.radius, 0+ball.radius],
            #                               [self.width-ball.radius, self.height-ball.radius],
            #                               ball.pos)
             
            #ball.pos = trimmed[0]

            #if trimmed[1][0]:
            #    ball.velocity[0] *= -1
            #if trimmed[1][1]:
            #    ball.velocity[1] *= -1

            ball.acceleration = np.multiply(ball.acceleration, 0)
            ball.aAcceleration = 0.001

    def display_logic(self):
        for ball in self.balls:
            print(f"ID: {ball.id}\nBall point: {ball.points}\n")
            ball.draw(self.screen)
            pygame.draw.circle(self.screen, self.colours["white"], ball.find_centroid().astype(int), 2)
        self.centre_ball.draw(self.screen)

def main():
    width, height = 600, 600 
    game = Game(5, width, height, width, height)
    game.main()

if __name__ == "__main__":
    main()

