import pygame
import numpy as np
from math import * 

class Animation():
    def __init__(self, width, height, fps=30, background="black", refresh_bg=True):
        """
            Initialise

            int width:  Width of screen
            int height: Height of screen

            string background:  Background of the display
            boolean refresh_bg: Refresh the background colour

            int fps:            The frame rate to cap. 
            string Background:  The background colour

            bool refresh_bg:    Whether or not to overwrite the background constantly

            return None
        """

        self.width   = width
        self.height  = height
        self.colours = {
                "black": [0x00, 0x00, 0x00],
                "white": [0xff, 0xff, 0xff],
                "red":   [0xff, 0x00, 0x00],
                "green": [0x00, 0xff, 0x00],
                "blue" : [0x00, 0x00, 0xff]
                }

        self.background     = self.colours[background]
        self.refresh_bg     = refresh_bg

        self.display        = pygame.display
        self.screen         = self.display.set_mode((self.width, self.height))
        
        self.clock          = pygame.time.Clock()
        self.fps            = fps
        self.frame_count    = 0 

        self.running = True

    def edit_colour(self, name, colour):
        """
            Add or change colour

            string name:    Name of colour to save in dictionary
            list   colour:  Colour values in form [int x, int x, int x]

            return None
        
        
        """
        self.colours[name] = colour

    def event_logic(self, event):
        """
            Defines the events logic 

            int event:      pygame event

            return None
        """
        
        if event.type == pygame.QUIT:
            exit()

    def game_logic(self):
        """
            The main game logic

            return None
        """

        pass
    
    def update_background(self):
        """
            Draws background image

            return None
        """

        self.screen.fill(self.background)
    
    def display_logic(self):
        """
            Drawing images / sprites etc...

            return None
        """

        pass

    def update(self):
        """
            Updates screen drawing

            return None
        """
        
        self.clock.tick(self.fps)
        self.display.update()

    def main(self):
        """
            The main body of the program

            return None
        """

        pygame.init()
        
        self.update_background()
        while self.running:
            if self.refresh_bg:
                self.update_background()

            for event in pygame.event.get():
                self.event_logic(event)
        
            self.game_logic()
            
            self.display_logic()
            self.update()
            self.frame_count += 1


def trim(minimum, maximum, to_trim):
    """
        Trims a list to min and max and checks for boundary touched 

        minimum -> e.g. [0, 10]
        maximum -> e.g. [600, 900]
        to_trim (same dimensions) -> e.g. [20, 4]

        list minimum: The list of minimums in respective order
        list maxmum:  The list of maxmums in respective order
        list to_trim: The list to trim

        return tuple(list, int, int) 
		
        trimmed list and if touching edges
        0 = no    boundary touched
        1 = lower boundary touched
        2 = upper boundary touched
    """

    edges = []
    for i in range(len(to_trim)):
        if to_trim[i] > maximum[i]:
            to_trim[i] = maximum[i]
            edges.append(2)
        elif to_trim[i] < minimum[i]:
            to_trim[i] = minimum[i]
            edges.append(1)
        else:
            edges.append(0)

    return to_trim, edges

def magnitude(vector):
    """
        Finds the magnitude of a vector 
        a^2 + b^2 = c^2

        return int
    """
    
    return np.linalg.norm(vector)

def normalise(vector):
    """
        Normalises the vector to length 1
        unit = 1/mag * vector

        return np.array
    """

    mag = magnitude(vector)
    if mag > 0:
        vector = np.divide(vector, mag)
    return vector

def map_range(x, input_start, input_end, output_start, output_end):
    """
        Maps a value of one function onto another function

        float x: Value to be mapped

        float input_start: Initial function start
        float input_end:   Initial function end

        float output_start: To map to function start
        float output_end:   To map to function end

        return float
        Mapped value x
    """

    return output_start + ((output_end - output_start) / (input_end - input_start)) * (x - input_start)

def rad(n):
    """
        Converts a degree number to radians
        
        float n: Number to convert

        return float
    """

    return n * 180 / pi

def deg(n):
    """
        Converts a radian number to degrees 
        
        float n: Number to convert

        return float
    """

    return n * pi / 180
