#!/usr/bin/env python
from animationLib import *
from objects import Ball 
from random import randint, uniform, choice

class Game(Animation):
    def __init__(self, number, x_range, y_range, width, height, fps=30, background="black", gravity=9.81):
        super().__init__(width, height, fps, background )
        
        allowed_colours = list(self.colours.keys())
        allowed_colours.remove('black')

        self.balls = [Ball(1,
                      self.colours[choice(allowed_colours)],
                      (randint(40,self.width-100), 60),
                      id=i,
                      radius=3)
                      for i in range(number)]

        self.centre_ball = Ball(2, self.colours["red"], (self.width / 2, self.height/ 2), id=69, radius=10)
    
    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
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

            force = ball.apply_gravitation_attraction(1, self.centre_ball.mass, self.centre_ball.pos)
            #self.centre_ball.apply_gravitation_attraction(0.0001, ball.mass, ball.pos)
            print(force)

            #if ball.pos[1] == self.height - ball.radius:
            #    ball.apply_friction(0.1, gravity)

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

            print(f"ID: {ball.id}\n\tVelocity: {ball.velocity}\n\tAcceleration: {ball.acceleration}\n\t(x,y): {ball.pos}\n\tmass: {ball.mass}\n\tTouching {ball.pos[1] == self.height - ball.radius}")
            ball.acceleration = np.multiply(ball.acceleration, 0)
            
        
    def display_logic(self):
        for ball in self.balls:
            ball.draw(self.screen)
        self.centre_ball.draw(self.screen)

def main():
    width, height = 1200, 600 
    game = Game(5, width, height, width, height)
    game.main()

if __name__ == "__main__":
    main()

