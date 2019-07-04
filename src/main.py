#!/usr/bin/env python
from animationLib import *
from objects import * 

class Pendulum():
    def __init__(self, origin, length, colour, radius=20, mass_multiplicative=0):
        """
            Initialisation

            Tuple(x,y) origin:  The start of the pendulum string
            float length:       The length of the pendulum rope
            float radius:       Radius of the pendulum ball

            float mass_multiplicative: The multiplicative onto radius to calculate mass (leave as 0 to keep it as a constant)

            return None
        """
        self.colour = colour

        self.origin = origin
        self.length = length
        self.radius = radius

        self.mass_multiplicative = mass_multiplicative if mass_multiplicative else 1

        self.angle          = 0
        self.aVelocity      = 0
        self.aAcceleration  = 0
    
    def find_ball_pos(self):
        """
            Calculates the ball position on pendulum

            return Tuple(x,y)
            Position of ball
        """

        change = np.multiply(self.length, (sin(self.angle), cos(self.angle)))
        return np.add(self.origin, change)
    
    def move(self, gravity=1):
        """
            Moves pendulum 

            float gravity: gravity constant
            
            return None
        """

        self.aAcceleration = -1 * gravity * sin(self.angle)

    def angle_from_pos(self, position):
        """
            Returns angle so that it can calculate new position

            Tuple(x,y) position: position to move ball to 
            
            return float 
            angle
        """
        
        difference = np.subtract(self.origin, position)
        print(f"Difference: {difference}")
        return acos(difference[1] / self.length) if difference[1] >= 0 else asin(difference[0] / self.length)

    def update(self):
        """
            Updates the angle based on rotation

            return None
        """

        self.angle      += self.aVelocity
        self.aVelocity  += self.aAcceleration

    def draw(self, screen, colour=[0xff, 0xff, 0xff]):
        """
            Draws the string and ball 
            
            pygame.Surface screen:  Screen to draw to
            list colour:            Colour to draw line
            
            return None
        """

        ball_pos = np.round(self.find_ball_pos()).astype(int)

        pygame.draw.line(screen, colour, self.origin, ball_pos)
        pygame.draw.circle(screen, self.colour, ball_pos, self.radius)


class Game(Animation):
    def __init__(self, dimensions, width, height, fps=30, background="black"):
        super().__init__(width, height, fps, background)
        
        self.pendulum = Pendulum((width/2, height/2), 150, self.colours["red"])
        self.pendulum.angle = deg(90)

    def event_logic(self, event):
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Angle: {self.pendulum.angle_from_pos(pygame.mouse.get_pos())}\n")

    def game_logic(self):
        self.pendulum.move(0.1)
        self.pendulum.aVelocity *= 0.9
        self.pendulum.update() 

    def display_logic(self):    
       self.pendulum.draw(self.screen) 

def main():
    width, height = 600, 600 
    game = Game((200,200,100,50), width, height)
    game.main()

if __name__ == "__main__":
    main()

