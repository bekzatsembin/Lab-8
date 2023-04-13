import pygame

import math

pygame.init()
clock = pygame.time.Clock()
# Set the width and height of the screen
WIDTH, HEIGHT = 800, 700

# Create a display surface and set its dimensions to WIDTH x HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define some colors using RGB values
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GRAY = pygame.Color(127, 127, 127)

# Define a base class for game objects
class GameObject:
    # Define a draw method that will be overridden by subclasses
    def draw(self):
        raise NotImplementedError
        
    # Define a handle method that will be overridden by subclasses
    def handle(self):
        raise NotImplementedError

# Define a Button class that inherits from the Sprite class
class Button(pygame.sprite.Sprite):
    # Initialize the button with a list of points that define its shape, 
    # a width for its outline (defaulting to 0), and a color (defaulting to GRAY)
    def __init__(self, points, width=0, color=GRAY):
        super().__init__()
        self.points = points
        self.width  = width
        self.color = color
        # Draw the polygon and assign the resulting rect to self.rect
        self.rect = pygame.draw.polygon(SCREEN, self.color, self.points, self.width)
    
    # Define a draw method that will draw the button to the screen
    def draw(self):    
        pygame.draw.polygon(SCREEN, self.color, self.points, self.width)

class Pen(GameObject):
    def __init__(self, start_pos, thickness=5, color=WHITE):
        # Initialize the properties of the Pen object
        self.thickness = thickness
        self.color = color
        self.points = [] 

    def draw(self):
        # Draw a line segment between each pair of consecutive points in the list of points
        for idx, point in enumerate(self.points[:-1]):
            pygame.draw.line(
                SCREEN,
                self.color,
                start_pos=point, 
                end_pos=self.points[idx + 1],
                width=self.thickness,
            )

    def handle(self, mouse_pos):
        # Add the current mouse position to the list of points
        self.points.append(mouse_pos)
        
        
class Rectangle(GameObject):
    def __init__(self, start_pos, thickness=5, color=WHITE):
        # Initialize the properties of the Rectangle object
        self.thickness = thickness
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos
    def draw(self):
        #start positions
        x1 = min(self.start_pos[0], self.end_pos[0])
        y1 = min(self.start_pos[1], self.end_pos[1])
        #end positions
        x2 = max(self.start_pos[0], self.end_pos[0])
        y2 = max(self.start_pos[1], self.end_pos[1])

        
        pygame.draw.rect(SCREEN, self.color, (x1, y1, x2 - x1, y2 - y1), width=self.thickness)
# This draws a rectangle on the SCREEN with the given color, position, and thickness.
    def handle(self, mouse_pos):
        self.end_pos = mouse_pos


class RightTriangle(GameObject):
    def __init__(self, start_pos, thickness=5, color=WHITE):
        self.thickness = thickness
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos

    def draw(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        

        vertex_1 = (x1, y1)
        vertex_2 = (x2, y2)
        vertex_3 = ((x2-x1)*math.cos(3.14/3)-(y2-y1)*math.sin(3.14/3)+x1, (x2-x1)*math.sin(3.14/3)+(y2-y1)*math.cos(3.14/3)+y1)
        vertices = [vertex_1, vertex_2, vertex_3]
        # This defines the vertices of the triangle using the start and end positions.

        pygame.draw.polygon(SCREEN, self.color, vertices, width=self.thickness)
        # This draws the triangle on the SCREEN with the given color and thickness.

    def handle(self, mouse_pos):
        self.end_pos = mouse_pos
        # This function updates the end position of the shape to the current mouse position.

class EquilateralTriangle(GameObject):
    def __init__(self, start_pos, thickness=5, color=WHITE):
        self.thickness = thickness
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos

    def draw(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos
        w = (x2 - x1) *2
        # This calculates the width of the equilateral triangle using the start and end positions.
        
        vertex_1 = (x1, y1)
        vertex_2 = (x2, y2)
        vertex_3 = (x2-w, y2)  # the third vertex is calculated as x2 minus the width of the triangle
        vertices = [vertex_1, vertex_2, vertex_3]

        pygame.draw.polygon(SCREEN, self.color, vertices, width=self.thickness)

    def handle(self, mouse_pos):
        self.end_pos = mouse_pos

class Rhombus(GameObject):
    def __init__(self, start_pos, thickness=5, color=WHITE):
        self.thickness = thickness
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos
    def draw(self):
        x1, y1 = self.start_pos
        x2, y2 = self.end_pos

        side_len = math.pow((x2-x1)**2 + (y2-y1)**2, 0.5) # calculate the length of a side using the distance formula
        x3 = (x2-x1)*math.cos(3.14/3)-(y2-y1)*math.sin(3.14/3)+x1
        y3 = (x2-x1)*math.sin(3.14/3)+(y2-y1)*math.cos(3.14/3)+y1
        x4 = (x2-x3)*math.cos(3.14/3)+(y2-y3)*math.sin(3.14/3)+x3
        y4 = (x2-x3)*math.sin(3.14/3)-(y2-y3)*math.cos(3.14/3)+y3
        vertex_1 = (x1, y1)
        vertex_2 = (x2, y2)
        vertex_3 = (x3, y3) # the third vertex is calculated by adding the length of a side to x2
        vertex_4 = (x4, y4) # the fourth vertex is calculated by adding the length of a side to x1
        vertices = [vertex_1, vertex_2, vertex_3, vertex_4]
        
        pygame.draw.polygon(SCREEN, self.color, vertices, width=self.thickness)
    def handle(self, mouse_pos):
        self.end_pos = mouse_pos
def main():
    # Define the points for the buttons that allow the user to select a shape
    Points_P   = [(28, 10), (12, 50)]  # Pen button
    Points_S   = [(50, 10), (90, 10), (90, 50), (50, 50)]  # Square button
    Points_RT  = [(135, 10), (170, 50), (100, 50)]  # Right triangle button
    Points_EqT = [(195, 10), (210, 50), (180, 50)]  # Equilateral triangle button
    Points_rh  = [(240, 10), (260, 30), (240, 50), (220, 30)]  # Rhombus button

    # Create instances of the Button class for each of the shape buttons
    switch_pen       = Button(Points_P, 5)
    switch_square    = Button(Points_S)
    switch_triangleR = Button(Points_RT)
    switch_triangleW = Button(Points_EqT)
    switch_rhombus   = Button(Points_rh)

    # Store the shape buttons in a list for easy iteration later
    buttons = [switch_pen,switch_square,switch_triangleR,switch_triangleW,switch_rhombus,]

    # Set the default shape to be the pen
    current_shape = 'pen'

    # Create an empty list to store the shapes the user has drawn
    objects = []

    # Create a variable to store the active shape that the user is currently drawing
    active_obj = None

    # Set up the game loop
    running = True
    while running:
        # Clear the screen
        SCREEN.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Define a dictionary that maps each button to its corresponding shape
                buttons_dict = {
                    switch_pen       :'pen',
                    switch_square    :'square',
                    switch_triangleR :'rightT',
                    switch_triangleW :'wrongT',
                    switch_rhombus   :'rhombus',
                }

                # Check which button the user clicked on and update the current_shape variable accordingly
                for key in buttons_dict.keys():
                    if key.rect.collidepoint(pygame.mouse.get_pos()):
                        current_shape = buttons_dict[key]

                # If the user clicked outside of the buttons, create a new instance of the selected shape class
                else:
                    shapes = {
                        'pen'    : Pen(start_pos=event.pos), 
                        'square' : Rectangle(start_pos=event.pos),
                        'rightT' : RightTriangle(start_pos=event.pos),
                        'wrongT' : EquilateralTriangle(start_pos=event.pos),
                        'rhombus': Rhombus(start_pos=event.pos),
                    }
                    active_obj = shapes[current_shape]

            # Handle mouse movement
            if event.type == pygame.MOUSEMOTION and active_obj is not None:
                active_obj.handle(mouse_pos=pygame.mouse.get_pos())
                active_obj.draw()

            # Handle mouse button release
            if event.type == pygame.MOUSEBUTTONUP and active_obj is not None:
                objects.append(active_obj)
                active_obj = None

        # Draw the buttons
        for button in buttons:
            button.draw()

        # Draw the shapes the user has drawn
        for obj in objects:
            obj.draw()

        # Tick the clock and update the display
        clock.tick(30)
        pygame.display.flip()

if __name__ == '__main__':
    main()