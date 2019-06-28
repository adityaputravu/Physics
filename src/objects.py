from animationLib import *

class Ball():
    def __init__(self, mass, colour, pos, id=None, mass_multiplicative=10, radius=None):
        """
            Intialise values

            int mass:                   mass of object
            string colour:              colour of object
            tuple(x,y) position:        position of object (starting)
            int id:                     id number 
            float mass_multiplicative:   the relationship between mass and displayed size

            return None
        """

        self.mass           = mass
        self.colour         = colour
        self.pos            = pos
        self.starting_pos   = pos
        self.id             = id

        self.radius         = mass * mass_multiplicative if not radius else radius

        self.velocity       = (0, 0)
        self.acceleration   = (0, 0)

        self.angle          = 0
        self.aVelocity      = 0
        self.aAcceleration  = 0

    def update(self):
        """
            Updates velocity and position

            return None
        """

        self.angle     += self.aVelocity
        self.aVelocity += self.aAcceleration

        self.velocity = np.add(self.velocity, self.acceleration)
        self.pos      = np.add(self.pos, self.velocity)

    def apply_force(self, force):
        """
            Applying a force to the object
            
            tuple(x, y) force:  the force to apply

            return None
        """

        force = np.divide(force, self.mass)
        self.acceleration = np.add(self.acceleration, force)

    def apply_fluid_resistance(self, rho, Cd):
        """
            Calculating fluid resistance

            fluid resistance =  - (fluid density * coeffecient of drag * surface area * v^2) / 2
                             = -1/2 * rho * Cd * surface area * ||v||^2 * v^
        
            float rho:  Density of fluid
            float Cd:   Coefficient of drag

            return None
        """

        area = pi * self.radius * 2 
        air_resistance = -0.5 * rho * Cd * area * pow(magnitude(self.velocity),2)
        air_resistance = np.multiply(air_resistance, normalise(self.velocity))
        self.apply_force(air_resistance)

    def apply_gravity(self, g):
        """
            Calculating weight force on object
            w = mg

            tuple(x,y) g:    Gravitational Field Strength

            return None
        """

        g = np.multiply(g, self.mass)
        self.apply_force(g)

    def apply_gravitation_attraction(self, g, mass, pos):
        """
            Calculates the gravitational attraction to another object
            
            Fg = (G * m1 * m2 / d^2) * r^

               = (G * m1 * m2 / ||r||^2) * r^
            G->gravitational field strength
            m1,m2->mass1,mass2
            r->distance unit vector
        
            float 	   g:       Gravitational Field Strength
            float 	   mass:    Mass of the other object
            tuple(x,y) pos: 	Position of second object   
            
            return None
        """
        r = np.subtract(pos, self.pos)
        d = magnitude(r)
        d = np.clip(d, 0.5, 2.5)
        force = (g * self.mass * mass) / (d*d)
        force = np.multiply(force, normalise(r))
        self.apply_force(force)
        return force

    def apply_friction(self, mew, g, angle=0):
        """
            Calculating force caused by friction

            friction = -mew * N
                     = -mew * ||N|| * v^
            N = -mgcos(theta)
            
            float mew:      Coefficient of friction
            tuple(x,y) g:   Gravitational Field Strength
            float angle:    Angle of elevation of surface

            return None
        """

        friction = -1 * mew * magnitude(np.multiply(-1 * self.mass * cos(angle), g))
        friction = np.multiply(friction, normalise(self.velocity))
        self.apply_force(friction)

    def draw(self, screen):
        """
            Draws ball to given screen

            pygame.Surface screen:  Screen to draw to 
            
            return None
        """

        pygame.draw.circle(screen, self.colour, np.round(self.pos).astype(int), round(self.radius))

    def draw_line(self, screen, colour=[0xff, 0xff, 0xff]):
        """
            Draws the attachment line from self.starting_pos to self.pos

            pygame.Surface screen: Screen to draw to
            list           colour: Colour to draw "string" as 

            return None
        """

        pygame.draw.line(screen, colour, np.round(self.starting_pos).astype(int), np.round(self.pos).astype(int))
    
    def moving(self, accuracy=0):
        """
            Moves the object based on mouse pointer (BETA)

            int accuracy:   Maximum range to allow deviation off the object

            return boolean
            Moving?
        """

        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            if self.check_boundaries(mouse, accuracy):
                self.pos = mouse
                return True
        return False

    def check_boundaries(self, pos, accuracy=0):
        """
            Checks the position values and whether they are within right boundaries
            
            tuple(x,y) pos:     	   Position to compare to ball position
            int 	   accuracy:       Maximum range to allow deviation off the position of object

            return boolean
            Success or False
        """

        distance = sqrt(pow(pos[0] - self.pos[0], 2) + pow(pos[1] - self.pos[1], 2))
        return True if distance < self.radius + accuracy else False


class Polygon():
    def __init__(self, pointlist, colour, mass=1, id=None):
        """
            Initialise

            list vector(x,y) pointlist: List of points of polygon

            string 			 colour: 	Colour of polygon
            int                 	 mass: 		mass of object
            int                          id:            Id number of rect

            return None
        """

        self.points = pointlist
        self.colour = colour
        
        self.mass = mass

        self.id   = id
        
        self.area = self.find_area()

        self.velocity =     (0,0)
        self.acceleration = (0,0)

        self.angle          = 0
        self.aVelocity      = 0 
        self.aAcceleration  = 0

    def draw(self, screen):
        """
            Draw polygon to screen

            pygame.Surface screen: The screen to draw image to

            return None
        """

        pygame.draw.polygon(screen, self.colour, self.points)

    def relative_points(self, r_point):
        """
            Get all the relative vector distances from r_point of polygon

            vector(x,y) r_point: Relative point to calculate distances from

            return list vector(x, y)
            Relative distances
        """

        return [np.subtract(p,r_point) for p in self.points]

    def translate(self, x, y):
        """
            Translate an object (x,y)

            int x: X direction
            int y: Y direction

            return None
        """

        for i in range(len(self.points)):
            self.points[i] = self.points[i][0] + x, self.points[i][1] + y 

    def rotate_clockwise(self, angle, r_point=(0,0)):
        """
            Rotate all points clockwise, around relative point
            Moves shape to origin, rotates and moves back
            
            [[cos -sin],
             [sin  cos]]	
            
            float 		  angle: Value to rotate (assumed radians)
            vector(x,y) r_point: relative point to rotate around

            return None
        """
        
        rotation = [[cos(angle), -sin(angle)],
                    [sin(angle),  cos(angle)]]
        
        points = self.relative_points(r_point)
        for i in range(len(points)):
            points[i] = np.dot(rotation, points[i]) 

        self.points = [p + r_point for p in points] 

    def rotate_anticlockwise(self, angle, r_point=(0,0)):
        """
            Rotate all points anit-clockwise, around relative point
            Moves shape to origin, rotates and moves back

            [[cos -sin],
             [sin  cos]]

            float angle: (assumed radians) Value to rotate
            vector(x,y) r_point: relative point to rotate around

            return None
        """

        rotation = [[ cos(angle), sin(angle)],
                    [-sin(angle), cos(angle)]]

        points = self.relative_points(r_point)
        for i in range(len(points)):
            points[i] = np.dot(rotation, points[i])

        self.points = [p + r_point for p in points] 
     
    def update(self):
        """
            Updates velocity and position and rotation

            return None
        """

        self.angle      += self.aVelocity
        self.aVelocity  += self.aAcceleration
        self.rotate_clockwise(self.angle, self.find_centroid())  # to do make it do it from centre

        self.velocity = np.add(self.velocity, self.acceleration)
        
        r_points 	= self.relative_points(self.points[0])
        pos      	= np.add(self.points[0], self.velocity)
        self.points = [np.add(r_points[i], pos) for i in range(len(self.points))]

    def apply_force(self, force):
        """
            Applying a force to the object
            
            tuple(x, y) force:  the force to apply

            return None
        """

        force = np.divide(force, self.mass)
        self.acceleration = np.add(self.acceleration, force)

    def apply_fluid_resistance(self, rho, Cd, area):
        """
            Calculating fluid resistance

            fluid resistance =  - (fluid density * coeffecient of drag * surface area * v^2) / 2
                             = -1/2 * rho * Cd * surface area * ||v||^2 * v^
        
            float rho:  Density of fluid
            float Cd:   Coefficient of drag
            float area: Area of polygon 

            return None
        """
        
        air_resistance = -0.5 * rho * Cd * area * pow(magnitude(self.velocity),2)
        air_resistance = np.multiply(air_resistance, normalise(self.velocity))
        self.apply_force(air_resistance)

    def apply_gravity(self, g):
        """
            Calculating weight force on object
            w = mg

            tuple(x,y) g:    Gravitational Field Strength

            return None
        """

        # w = mg 
        g = np.multiply(g, self.mass)
        self.apply_force(g)

    def apply_gravitation_attraction(self, g, mass, pos):
        """
            Calculates the gravitational attraction to another object
            
            Fg = (G * m1 * m2 / d^2) * r^

               = (G * m1 * m2 / ||r||^2) * r^
            G->gravitational field strength
            m1,m2->mass1,mass2
            r->distance unit vector
        
            float  	   g:        Gravitational Field Strength
            float 	   mass:     Mass of the other object
            tuple(x,y) pos: 	 Position of second object   
            
            return None
        """

        r = np.subtract(pos, self.points[0])
        d = magnitude(r)
        d = np.clip(d, 0.5, 2.5)
        force = (g * self.mass * mass) / (d*d)
        force = np.multiply(force, normalise(r))
        self.apply_force(force)
        return force

    def apply_friction(self, mew, g, angle=0):
        """
            Calculating force caused by friction

            friction = -mew * N
                     = -mew * ||N|| * v^
            N = -mgcos(theta)
            
            float 		mew:      Coefficient of friction
            tuple(x,y)  g:   	  Gravitational Field Strength
            float 		angle:    Angle of elevation of surface

            return None
        """

        friction = -1 * mew * magnitude(np.multiply(-1 * self.mass * cos(angle), g))
        friction = np.multiply(friction, normalise(self.velocity))

    def find_area(self):
        """
            Finds the area of any polygon

            1/2 * abs( sigma(i=1 to n) ( det [(x_i, y_i+1)
                                              (y_i, x_i+1)]
                                  ) )
            det = determinant = ad - bc
            
            return float
            Area
        """

        total = 0 
        for i in range(len(self.points)-1):
            (x,y),(x1,y1) = self.points[i],self.points[i+1]
            total += (x1 + x) * (y1 - y) 

        return 1/2 * abs(total)

    def find_centroid(self):
        """
            Finds the centroid of a non intersecting n-side polygon

            return float Tuple(x,y)
            Centroid coordinates
        """
        
        length = len(self.points)
        signedArea = 0
        centroid = (0, 0)
        for i in range(length):
            (x, y), (x1, y1) = self.points[i], self.points[(i+1) % length]
            a = x*y1 - x1*y
            signedArea += a
            centroid = np.add(centroid, ((x + x1) * a, (y + y1) * a))
                                                 
        signedArea *= 0.5
        if signedArea:
            centroid = np.divide(centroid, 6*signedArea) 
        else:
            centroid = np.asarray((0, 0))
        return centroid


class Rect(Polygon):
    def __init__(self, x, y, width, height, colour, id=0):
        """
            Initialise

            int x: starting x position of rectangle
            int y: starting y position of rectangle

            int width:  width of rectangle
            int height: height of rectangle

            string colour: colour of rectangle
            int    id:     Id of rectangle

            return None
        """

        pointlist = [(x,y), (x+width, y), (x+width, y+height), (x,y+height)]

        self.height = height
        self.width  = width 

        super().__init__(pointlist, colour, id=id)

    def get_dimensions(self):
        """
            Gets the (x,y) (width, height) of rect (when not rotated it works)

            return list tuple(x,y)
        """

        return self.points[0], np.subtract(self.points[2], self.points[0])

    def find_centroid(self):
        """
            Gets the centre of the rectangle
                        
            return tuple(x,y)
        """
                
        return np.divide(np.add(self.points[0], self.points[2]), 2)
