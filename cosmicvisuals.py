'''Cosmic Core: Cosmic Visuals
\n\tA library of functions using the `turtle` module to draw 2D shapes defined in `cosmicgeometry.py` and graph the polynomial object defined in `cosmicalgebra.py`.'''
import turtle
from .cosmicalgebra import *
from .cosmicgeometry import *
__all__ = ['draw', 'plotpolynomial', 'drawgrid']


#___Drawing Geometric Objects___
def draw(object, scale = 1.0, color = 'black', line_width = 1, fill = None):
    '''Draw a point, line, or 2D shape defined in `cosmicgeometry.py`.'''
    turtle.color(color)
    turtle.pensize(line_width)

    if isinstance(object, point):
        if object.is3d():
            raise ValueError('cannot draw 3D points')
        turtle.penup()
        turtle.goto(object.x * scale, object.y * scale)
        turtle.pendown()
        turtle.dot(5)
    
    elif isinstance(object, line):
        if object.isvertical():
            turtle.penup()
            turtle.goto(object.point1.x * scale, -turtle.window_height() / 2 * scale)
            turtle.pendown()
            turtle.goto(object.point1.x * scale, turtle.window_height() / 2 * scale)
        else:
            #Draw a line using slope-intercept form
            slope = object.slope()
            y_intercept = object.yintercept()

            # Calculate the x-coordinate of the leftmost and rightmost points
            leftmost_x = -turtle.window_width() / 2
            rightmost_x = turtle.window_width() / 2

            #Calculate the y-coordinates at the leftmost and rightmost points
            leftmost_y = slope * leftmost_x + y_intercept
            rightmost_y = slope * rightmost_x + y_intercept

            #Draw the line
            turtle.penup()
            turtle.goto(leftmost_x * scale, leftmost_y * scale)
            turtle.pendown()
            turtle.goto(rightmost_x * scale, rightmost_y * scale)

    elif isinstance(object, rectangle):
        if object.bottom_left is None:
            raise ValueError('rectangle must have coordinates to be drawn')
        bottom_left = object.bottom_left
        top_left = object.topleft()
        bottom_right = object.bottomright()
        top_right = object.topright()

        turtle.penup()
        turtle.goto(bottom_left.x * scale, bottom_left.y * scale)
        if fill is not None:
            turtle.fillcolor(fill)
            turtle.begin_fill()
        turtle.pendown()
        turtle.goto(top_left.x * scale, top_left.y * scale)
        turtle.goto(top_right.x * scale, top_right.y * scale)
        turtle.goto(bottom_right.x * scale, bottom_right.y * scale)
        turtle.goto(bottom_left.x * scale, bottom_left.y * scale)
        if fill is not None:
            turtle.end_fill()

    elif isinstance(object, circle):
        if object.center is None:
            raise ValueError('circle must have coordinates to be drawn')
        center = object.center
        radius = object.radius
        turtle.goto(center.x * scale, (center.y - radius) * scale)
        if fill is not None:
            turtle.fillcolor(fill)
            turtle.begin_fill()
        turtle.pendown()
        turtle.circle(radius * scale)
        if fill is not None:
            turtle.end_fill()

    elif isinstance(object, triangle):
        point1 = object.point1
        point2 = object.point2
        point3 = object.point3
        turtle.penup()
        turtle.goto(point1.x * scale, point1.y * scale)
        if fill is not None:
            turtle.fillcolor(fill)
            turtle.begin_fill()
        turtle.pendown()
        turtle.goto(point2.x * scale, point2.y * scale)
        turtle.goto(point3.x * scale, point3.y * scale)
        turtle.goto(point1.x * scale, point1.y * scale)
        if fill is not None:
            turtle.end_fill()

    elif isinstance(object, polygon):
        if len(object.vertices) < 3:
            raise ValueError('polygon must have at least 3 vertices')
        turtle.penup()
        turtle.goto(object.vertices[0].x * scale, object.vertices[0].y * scale)
        if fill is not None:
            turtle.fillcolor(fill)
            turtle.begin_fill()
        turtle.pendown()
        for vertex in object.vertices[1:]:
            turtle.goto(vertex.x * scale, vertex.y * scale)
        turtle.goto(object.vertices[0].x * scale, object.vertices[0].y * scale)
        if fill is not None:
            turtle.end_fill()

    else:
        raise TypeError(f'unsupported object type: {type(object)}')
        
    turtle.penup()


#___Plotting Polynomials___
def plotpolynomial(poly, scale = 1.0, color='black', line_width=1):
    '''Plot a polynomial across the entire Turtle screen.'''
    if not isinstance(poly, polynomial):
        raise TypeError('poly must be a polynomial')
    turtle.speed(0)
    turtle.hideturtle()

    screen = turtle.Screen()
    screen_width = screen.window_width()
    screen_height = screen.window_height()

    drawing_width = screen_width / 2

    turtle.color(color)
    turtle.pensize(line_width)

    if poly.degree() == 0:
        drawline = line(point(0, poly.coefficients[0]), point(1, poly.coefficients[0]))
        draw(drawline, scale, color, line_width) 

    elif poly.degree() == 1:
        drawline = generateline(poly)
        draw(drawline, scale, color, line_width)

    else:
        #For higher-degree polynomials, use the standard plotting method
        turtle.penup()
        turtle.goto(-drawing_width, poly.evaluate(-drawing_width / scale) * scale)  #Start point
        turtle.pendown()

        #Iterate through x-values within the screen bounds
        for x in range(-int(drawing_width), int(drawing_width) + 1, 1):
            #Calculate the y-value, stretched both horizontally and vertically
            y = poly.evaluate(x / scale) * scale

            #Only draw if the y-value is within the screen bounds
            if -screen_height / 2 <= y <= screen_height / 2:
                turtle.goto(x, y) 

    turtle.penup()



#___Drawing a Grid___
def drawgrid(scale, grid_color='light gray', axes_color='black'):
    '''Draw a grid on the screen.'''
    turtle.speed(0)
    turtle.pensize(1)
    turtle.hideturtle()
    turtle.penup()

    screen = turtle.Screen()
    screen_width = screen.window_width()
    screen_height = screen.window_height()

    # Calculate the usable drawing area (center of screen)
    drawing_width = screen_width / 2
    drawing_height = screen_height / 2

    left_edge = -int(drawing_width / scale) * scale 
    right_edge = int(drawing_width / scale) * scale
    bottom_edge = -int(drawing_height / scale) * scale
    top_edge = int(drawing_height / scale) * scale

    turtle.color(grid_color)
    turtle.penup()

    # Draw vertical lines
    for y in range(bottom_edge, top_edge + 1, scale):
        turtle.goto(-drawing_width, y)
        turtle.pendown()
        turtle.goto(drawing_width, y)
        turtle.penup()

    # Draw horizontal lines
    for x in range(left_edge, right_edge + 1, scale):
        turtle.goto(x, -drawing_height)
        turtle.pendown()
        turtle.goto(x, drawing_height)
        turtle.penup()

    # Draw origin axes (black)
    turtle.color(axes_color)
    turtle.goto(-drawing_width, 0)
    turtle.pendown()
    turtle.goto(drawing_width, 0)
    turtle.penup()
    turtle.goto(0, -drawing_height)
    turtle.pendown()
    turtle.goto(0, drawing_height)
    turtle.penup()