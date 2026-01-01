'''Cosmic Core: Cosmic Geometry
\n\tA library of data types and functions built to simplify geometry.'''
from .cosmicalgebra import *
from .cosmicdatastructures import *
from .cosmicmath import *
from numpy import ndarray
__all__ = ['point', 'vector', 'line', 'shape2d', 'rectangle', 'circle',
           'triangle', 'polygon', 'rectangularprism', 'sphere', 'generateline']


#___Fundamental Objects___
class point(object):
    '''Represents a point on a two-dimensional or three-dimensional plane.'''
    
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z
    
    def is3d(self):
        '''Return True if z has a value, False otherwise.'''
        return self.z is not None
    
    def distance(self, other):
        '''Return the distance between two points.'''
        if not isinstance(other, point):
            raise TypeError('other must be a point')
        if self.is3d() and other.is3d():
            return sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2) 
                        + pow(other.z - self.z, 2))
        elif not self.is3d() and not other.is3d():
            return sqrt(pow(other.x - self.x, 2) + pow(other.y - self.y, 2))
        else:
            raise ValueError('points must be in the same dimension')
    
    def midpoint(self, other):
        '''Return the midpoint between two points.'''
        if not isinstance(other, point):
            raise TypeError('other must be a point')
        if self.is3d() and other.is3d():
            return point(average([self.x, other.x]), average([self.y, other.y]), 
                         average([self.z, other.z]))
        elif not self.is3d() and not other.is3d():            
            return point(average([self.x, other.x]), average([self.y, other.y]))
        else:
            raise ValueError('points must be in the same dimension')
    
    def translate(self, dx, dy, dz = 0):
        '''Move the point by a given displacement.'''
        self.x += dx
        self.y += dy
        if self.is3d():
            self.z += dz

    def scale(self, factor):
        '''Scale the point by a given factor.'''
        self.x *= factor
        self.y *= factor
        if self.is3d():
            self.z*= factor
    
    def __str__(self):
        '''Return the string representation of the point.'''
        if self.is3d():
            return f'({self.x}, {self.y}, {self.z})'
        else:
            return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return 'point' + str(self)
    
    def __eq__(self, other):
        '''Check to see if two points are identical.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
class vector(object):
    '''Represents a vector in a two-dimensional or three-dimensional plane.'''
    
    def __init__(self, x, y, z = None):
        self.x = x
        self.y = y
        self.z = z
    
    def is3d(self):
        '''Return True if z has a value, False otherwise.'''
        return self.z is not None
    
    def magnitude(self):
        '''Calculate the magnitude (length) of the vector.'''
        if self.is3d:
            return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))
        else:
            return sqrt(pow(self.x, 2) + pow(self.y, 2))
    
    def normalize(self):
        '''Return a normalized vector.'''
        magnitude = self.magnitude()
        if magnitude != 0:
            return vector(self.x / magnitude, self.y / magnitude, 
                          self.z / magnitude if self.is3d() else None)
        else:
            return vector(0, 0, 0)
    
    def dotproduct(self, other):
        '''Calculate the dot product with another vector.'''
        if not isinstance(other, vector):
            raise TypeError('other must be a vector')
        if self.is3d() and other.is3d():
            return (self.x * other.x) + (self.y * other.y) * (self.z * other.z)
        elif not self.is3d() and not other.is3d():            
            return (self.x * other.x) + (self.y * other.y)
        else:
            raise ValueError('vectors must be in the same dimension')

    def crossproduct(self,other):
        '''Calculate the cross product with another vector.
        \nPrecondition: Both vectors are three-dimensional.'''
        if not isinstance(other, vector):
            raise TypeError('other must be a vector')
        if self.is3d() and other.is3d():
            return vector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        else:
            raise ValueError('cross product is only defined for 3D vectors')

    def __str__(self):
        '''Return the string representation of the vector.'''
        if self.is3d():
            return f'({self.x}, {self.y}, {self.z})'
        else:
            return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return 'vector' + str(self)
    
    def __eq__(self, other):
        '''Check to see if two vectors are identical.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        '''Add two vectors.'''
        if not isinstance(other, vector):
            raise TypeError('can only add vectors to other vectors') 
        if self.is3d() and other.is3d():
            return vector(self.x + other.x, self.y + other.y, self.z + other.z)
        elif not self.is3d() and not other.is3d():
            return vector(self.x + other.x, self.y + other.y)
        else:
            raise ValueError('vectors must be in the same dimension')

    def __sub__(self, other):
        '''Subtract two vectors.'''
        if not isinstance(other, vector):
            raise TypeError('can only add vectors to other vectors') 
        if self.is3d() and other.is3d():
            return vector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif not self.is3d() and not other.is3d():
            return vector(self.x - other.x, self.y - other.y)
        else:
            raise ValueError('vectors must be in the same dimension')

    def __mul__(self, scalar):
        '''Multiply a vector by a scalar.'''
        return vector(self.x * scalar, self.y * scalar, 
                      self.z * scalar if self.is3d() else None)
    
    def __rmul__(self,scalar):
        '''Multiply a vector by a scalar.'''
        return vector(self.x * scalar, self.y * scalar, 
                      self.z * scalar if self.is3d() else None)
    
class line(object):
    '''Represents a line in two-dimensional space.'''

    def __init__(self, point1, point2):
        if not isinstance(point1, point) or not isinstance(point2, point):
            raise TypeError('both points must be of type \'point\'')
        if point1 == point2:
            raise ValueError('the two points cannot be the same')
        if point1.is3d() or point2.is3d():
            raise ValueError('the two points must be in 2D space')
        self.point1 = point1
        self.point2 = point2
    
    def slope(self):
        '''Return the slope of the line.'''
        if self.point1.x == self.point2.x:
            return inf #Slope is undefined for vertical lines.
        else:
            return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
        
    def isvertical(self):
        '''Return True if the line is vertical, False otherwise.'''
        return self.slope() == inf
    
    def ishorizontal(self):
        '''Return True if the line is horizontal, False otherwise.'''
        return self.slope() == 0
        
    def yintercept(self):
        '''Return the y-intercept of the line.'''
        m = self.slope()
        if self.isvertical():  #Vertical line, y-intercept is undefined
            return None
        else:
            return self.point1.y - m * self.point1.x
        
    def isparallel(self, other):
        '''Check to see if two lines are parallel.'''
        if not isinstance(other, line):
            raise TypeError('other must be a line')
        return self.slope() == other.slope()
    
    def iscoincident(self, other):
        '''Check to see if two lines are coincident.'''
        if not isinstance(other, line):
            raise TypeError('other must be a line')    
        return self.slope() == other.slope() and self.yintercept() == other.yintercept()   
    
    def equation(self):
        '''Return the equation of the line in slope-intercept form.'''
        m = self.slope()
        b = self.yintercept()
        if self.isvertical():
            return f'x = {self.point1.x}'
        else:
            return f'y = {m}x + {b}'

    def intersection(self, other):
        '''Calculate the point of intersection between two lines.
        \nPreconditions: 
        \t1. other is a line
        \t2. the lines are not parallel
        \nPostcondition: 
        \t1. if the lines intersect, the intersection point is returned.
        \t2. if the lines do not intersect, None is returned.
        \t3. if the lines are coincident, self is returned.'''
        if not isinstance(other, line):
            raise TypeError('other must be a line')
        if self.isparallel(other):
            if self.iscoincident(other):
                return self #Coincident lines have infinitely many intersections
            else:
                return None #Parallel lines have no intersections
        m1 = self.slope()
        b1 = self.yintercept()
        m2 = other.slope()
        b2 = other.yintercept()

        if self.isvertical(): #Case for vertical line
            return point(self.point1.x, m2 * self.point1.x + b2)
        elif other.isvertical(): #Case for vertical line
            return point(other.point1.x, m1 * other.point1.x + b1)
        else: 
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
            return point(x, y)
        
    def __str__(self):
        '''Return the string representation of the line.'''
        return f'Line through points {self.point1} and {self.point2}'

    def __repr__(self):
        return f'line({self.point1}, {self.point2})'
    
    def __eq__(self, other):
        '''Check to see if two lines are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return (self.point1 == other.point1 and self.point2 == other.point2) or \
           (self.point1 == other.point2 and self.point2 == other.point1)

def generateline(poly):
    '''Generate a line object from a polynomial of degree 1.'''
    if not isinstance(poly, polynomial):
        raise TypeError("poly must be a polynomial object")
    if poly.degree() != 1:
        raise ValueError("polynomial must be of degree 1 to represent a line")
    slope = poly.coefficients[1]
    y_intercept = poly.coefficients[0]

    point1 = point(0, y_intercept)
    point2 = point(1, y_intercept + slope)

    return line(point1, point2)  

#___Two-Dimensional (2D) Geometric Shapes___
class shape2d(object):
    '''Generic base class for two-dimensional shapes.'''

    def __init__(self):
        pass

    def area(self):
        '''Calculate the area of the shape.'''
        raise NotImplementedError('area() must be implemented by subclasses')
    
    def perimeter(self):
        '''Calculate the perimeter of the shape.'''
        raise NotImplementedError('perimeter() must be implemented by subclasses')
    
    def contains(self, point):
        '''Return True if the point is inside the shape, False otherwise.'''
        raise NotImplementedError('contains() must be implemented by subclasses')
    
    def translate(self, dx, dy):
        '''Move the shape by a given displacement.'''
        raise NotImplementedError('translate() must be implemented by subclasses')
    
    def scale(self, factor):
        '''Scale the shape by a given factor.'''
        raise NotImplementedError('scale() must be implemented by subclasses')
    
    def iscongruent(self, other):
        '''Check to see if two shapes are congruent (same size and shape).'''
        raise NotImplementedError('iscongruent() must be implemented by subclasses')
    
    def __str__(self):
        '''A string representation of the shape.'''
        return '2D Shape'
    
    def __repr__(self):
        return 'shape2d()'
    
    def __eq__(self, other):
        '''Check to see if two shapes are equal.'''
        if self is other:
            return True
        if isinstance(other, shape2d):
            return True
        return False
    
class rectangle(shape2d):
    '''Represents a rectangle in a two-dimensional space. Can also represent a
    square if the width and height are equal.'''

    def __init__(self, width, height, bottom_left = None):
        if bottom_left is not None:
            if not isinstance(bottom_left, point):
                raise TypeError('bottom_left must be of type \'point\'')
            if bottom_left.is3d():
                raise ValueError('bottom_left must be in 2D space')
        self.width = width
        self.height = height
        self.bottom_left = bottom_left

    def topleft(self):
        '''Return the top left corner of a rectangle.'''
        return point(self.bottom_left.x, self.bottom_left.y + self.height)
    
    def bottomright(self):
        '''Return the bottom right corner of a rectangle.'''
        return point(self.bottom_left.x + self.width, self.bottom_left.y) 
    
    def topright(self):
        '''Return the top right corner of a rectangle.'''
        return point(self.bottom_left.x + self.width, self.bottom_left.y + self.height)   

    def center(self):
        '''Return the center point of a rectangle.'''
        return point(self.bottom_left.x + (self.width / 2), self.bottom_left.y + (self.height / 2))
    
    def area(self):
        '''Calculate the area of the rectangle.'''
        return self.width * self.height
    
    def perimeter(self):
        '''Calculate the perimeter of the rectangle.'''
        return 2 * (self.width + self.height)
    
    def contains(self, point):
        '''Return True if the point is inside the rectangle, False otherwise.'''
        if self.bottom_left is None:
            raise ValueError('bottom_left must be defined to check containment')
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if point.is3d():
            raise ValueError('point must be in 2D space')
        return (self.bottom_left.x <= point.x <= self.bottom_left.x + self.width and \
                self.bottom_left.y <= point.y <= self.bottom_left.y + self.height)

    def diagonal(self):
        '''Calculate the diagonal of the rectangle.'''
        return sqrt(pow(self.width, 2) + pow(self.height, 2))

    def translate(self, dx, dy):
        '''Move the rectangle by a given displacement.'''
        if self.bottom_left is not None:
            self.bottom_left.translate(dx, dy)
    
    def scale(self, factor):
        '''Scale the rectangle by a given factor.'''   
        self.width *= factor
        self.height *= factor
        if self.bottom_left is not None:
            self.bottom_left.scale(factor)

    def iscongruent(self, other):
        '''Check to see if two rectangles are congruent (same width and height).'''
        if not isinstance(other, rectangle):
            raise TypeError('other must be a rectangle')
        return (self.width == other.width and self.height == other.height) or \
                (self.width == other.height and self.height == other.width)
    
    def issquare(self):
        '''Check to see if the rectangle is a square.'''
        return self.width == self.height
    
    def __eq__(self, other):
        '''Check to see if two rectangles are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.width == other.width and self.height == other.height and \
                self.bottom_left == other.bottom_left
    
    def __str__(self):
        '''A string representation of the rectangle.'''
        if self.bottom_left is not None:
            if self.issquare():
                return f'Square with side length {self.width}, and bottom-left corner at {self.bottom_left}'
            else:
                return f'Rectangle with width {self.width}, height {self.height}, and bottom-left corner at {self.bottom_left}'
        else:
            if self.issquare():
                return f'Square with side length {self.width}'
            else:
                return f'Rectangle with width {self.width}, and height {self.height}'
    
    def __repr__(self):
        if self.bottom_left is not None:
            return f'rectangle({self.width}, {self.height}, {repr(self.bottom_left)})'
        else:
             return f'rectangle({self.width}, {self.height})'
        
class circle(shape2d):
    '''Represents a circle in a two-dimensional space.'''

    def __init__(self, radius, center = None):
        if center is not None:
            if not isinstance(center, point):
                raise TypeError('center must be of type \'point\'')
            if center.is3d():
                raise ValueError('center must be in 2D space')
        self.radius = radius
        self.center = center

    def diameter(self):
        '''Calculate the diameter of the circle.'''
        return self.radius * 2
    
    def circumference(self):
        '''Calculate the circumference of the circle.'''
        return 2 * PI * self.radius
    
    def area(self):
        '''Calculate the area of the circle.'''
        return PI * pow(self.radius, 2)
    
    def perimeter(self):
        '''Calculate the circumference of the circle.'''
        return self.circumference
    
    def contains(self, point):
        '''Return True if the point is inside the circle, False otherwise.'''
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if point.is3d():
            raise ValueError('point must be in 2D space')
        return self.center.distance(point) <= self.radius
    
    def translate(self, dx, dy):
        '''Move the circle by a given displacement.'''
        if self.center is not None:
            self.center.translate(dx, dy)    

    def scale(self, factor):
        '''Scale the circle by a given factor.'''
        self.radius *= factor
        if self.center is not None:
            self.center.scale(factor)
    
    def iscongruent(self, other):
        '''Check to see if two circles are congruent (same radius).'''
        if not isinstance(other, circle):
            raise TypeError('other must be a circle')
        return self.radius == other.radius

    def __str__(self):
        '''A string representation of the circle.'''
        if self.center is not None:
            return f'Circle with radius {self.radius}, and center at {self.center}'
        else:
            return f'Circle with radius {self.radius}'

    def __repr__(self):
        if self.center is not None:
            return f'circle({self.radius}, {repr(self.center)})'
        else:
             return f'circle({self.radius})'
        
    def __eq__(self, other):
        '''Check to see if two circles are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.radius == other.radius and self.center == other.center
    
class triangle(shape2d):
    '''Represents a triangle in a two-dimensional space.'''

    def __init__(self, point1, point2, point3):
        if not isinstance(point1, point) or not isinstance(point2, point) or not isinstance(point3, point):
            raise TypeError('all vertices must be of type \'point\'')
        if point1.is3d() or point2.is3d() or point3.is3d():
            raise ValueError('all vertices must be in 2D space')
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
    
    def area(self):
        '''Calculate the area of the triangle using Heron's formula.'''
        a = self.point1.distance(self.point2)
        b = self.point2.distance(self.point3)
        c = self.point3.distance(self.point1)
        s = (a + b + c) / 2  #Semi-perimeter
        return sqrt(s * (s - a) * (s - b) * (s - c))
    
    def perimeter(self):
        '''Calculate the perimeter of the triangle.'''
        return self.point1.distance(self.point2) + self.point2.distance(self.point3) + self.point3.distance(self.point1)
    
    def incenter(self):
        '''Calculate the incenter (intersection of angle bisectors) of the triangle.'''
        a = self.point1.distance(self.point2)
        b = self.point2.distance(self.point3)
        c = self.point3.distance(self.point1)
        x = (a * self.point1.x + b * self.point2.x + c * self.point3.x) / (a + b + c)
        y = (a * self.point1.y + b * self.point2.y + c * self.point3.y) / (a + b + c)
        return point(x, y)
    
    def centroid(self):
        '''Calculate the centroid (intersection of medians) of the triangle.'''
        return point((self.point1.x + self.point2.x + self.point3.x) / 3, 
                     (self.point1.y + self.point2.y + self.point3.y) / 3)
    
    def contains(self, point):
        '''Return True if the point is inside the triangle, False otherwise.'''
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if point.is3d():
            raise ValueError('point must be in 2D space')
        v1 = vector(self.point2.x - self.point1.x, self.point2.y - self.point1.y)
        v2 = vector(self.point3.x - self.point1.x, self.point3.y - self.point1.y)
        v3 = vector(point.x - self.point1.x, point.y - self.point1.y)
        u = ((v2.y * v3.x) - (v2.x * v3.y)) / ((v1.x * v2.y) - (v1.y * v2.x))
        v = ((v1.x * v3.y) - (v1.y * v3.x)) / ((v1.x * v2.y) - (v1.y * v2.x))
        w = 1 - u - v
        return 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1
    
    def translate(self, dx, dy):
        '''Move the triangle by a given displacement.'''
        self.point1.translate(dx, dy)
        self.point2.translate(dx, dy)
        self.point3.translate(dx, dy)

    def scale(self, factor):
        '''Scale the triangle by a given factor.'''
        self.point1.scale(factor)
        self.point2.scale(factor)
        self.point3.scale(factor)

    def iscongruent(self, other):
        '''Check to see if two triangles are congruent (side lengths are equal).'''
        if not isinstance(other, triangle):
            raise TypeError('other must be a triangle')
        a1 = self.point1.distance(self.point2)
        b1 = self.point2.distance(self.point3)
        c1 = self.point3.distance(self.point1)
        a2 = other.point1.distance(other.point2)
        b2 = other.point2.distance(other.point3)
        c2 = other.point3.distance(other.point1)    
        return a1 == a2 and b1 == b2 and c1 == c2
    
    def isequilateral(self):
        '''Check to see if the triangle is equilateral (all three side lengths are equal).'''
        return self.point1.distance(self.point2) == self.point2.distance(self.point3) == self.point3.distance(self.point1)
    
    def isisoceles(self):
        '''Check to see if the triangle is isoceles (two side lengths are equal).'''
        if self.isequilateral():
            return False
        a = self.point1.distance(self.point2)
        b = self.point2.distance(self.point3)
        c = self.point3.distance(self.point1)
        return a == b or b == c or c == a 
    
    def isscalene(self):
        '''Check to see if the triangle is scalene (all side lengths are different).'''
        return not self.isequilateral() and not self.isisoceles()
    
    def __str__(self):
        '''A string representation of the triangle.'''
        return f'Triangle with vertices: {self.point1}, {self.point2}, {self.point3}'

    def __repr__(self):
        return f'triangle({repr(self.point1)}, {repr(self.point2)}, {repr(self.point3)})'
    
    def __eq__(self, other):
        '''Check to see if two triangles are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.point1 == other.point1 and self.point2 == other.point2 and \
             self.point3 == other.point3
    
class polygon(shape2d):
    '''Represents a polygon in a two-dimensional space.'''

    def __init__(self, vertices):
        if type(vertices) not in (list, linklist, dlinklist, ndarray):
            raise TypeError('''vertices must be of type \'list\', \'linklist\',
                             \'dlinklist\', or \'ndarray\'''')
        if isinstance(vertices, ndarray):
            vertices = vertices.tolist()
        if not all(isinstance(vertex, point) for vertex in vertices):
            raise TypeError('all vertices must be of type \'point\'')
        if any(vertex.is3d() for vertex in vertices):
            raise ValueError('all vertices must be in 2D space')
        if len(vertices) < 3:
            raise ValueError('a polygon must have 3 vertices')
        self.vertices = vertices
    
    def area(self):
        '''Calculate the area of the polygon using the shoelace formula.'''
        n = len(self.vertices)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y - self.vertices[j].x * self.vertices[i].y
        return abs(area) / 2
    
    def perimeter(self):
        '''Calculate the perimeter of the polygon.'''
        perimeter = 0
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            perimeter += self.vertices[i].distance(self.vertices[j])
        return perimeter
    
    def contains(self, point):
        '''Return True if the point is inside the polygon, False otherwise.'''
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if point.is3d():
            raise ValueError('point must be in 2D space')
        crossings = 0
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            #Check if the horizontal ray from the point intersects an edge
            if (self.vertices[i].y <= point.y < self.vertices[j].y or 
                self.vertices[j].y <= point.y < self.vertices[i].y):
                #Calculate the x-coordinate of the intersection point
                intersection_x = self.vertices[i].x + (point.y - self.vertices[i].y) * (self.vertices[j].x - self.vertices[i].x) / (self.vertices[j].y - self.vertices[i].y)
                #Check if the intersection point is to the right of the point
                if intersection_x > point.x:
                    crossings += 1
        #Even number of crossings means the point is outside, odd means inside
        return crossings % 2 == 1
    
    def translate(self, dx, dy):
        '''Move the polygon by a given displacement.'''
        for vertex in self.vertices:
            vertex.translate(dx, dy)
    
    def scale(self, factor):
        '''Scale the polygon by a given factor.'''
        for vertex in self.vertices:
            vertex.scale(factor)

    def iscongruent(self, other):
        '''Check to see if two polygons are congruent (same sides).'''
        if not isinstance(other, polygon):
            raise TypeError('other must be a polygon')
        if len(self.vertices) != len(other.vertices):
            return False

        #Sort the vertices of both polygons
        sorted_vertices1 = sorted(self.vertices, key=lambda vertex: (vertex.x, vertex.y))
        sorted_vertices2 = sorted(other.vertices, key=lambda vertex: (vertex.x, vertex.y))

        #Compare side lengths in the same order
        for i in range(len(sorted_vertices1)):
            j = (i + 1) % len(sorted_vertices1)
            side1 = sorted_vertices1[i].distance(sorted_vertices1[j])
            side2 = sorted_vertices2[i].distance(sorted_vertices2[j])
            if not isclose(side1, side2):
                return False
    
    def __str__(self):
        '''A string representation of the polygon.'''
        vertices_str = ", ".join(f"({vertex.x}, {vertex.y})" for vertex in self.vertices)
        return f"Polygon with vertices: {vertices_str}"
    
    def __repr__(self):
        vertices_repr = ", ".join(repr(vertex) for vertex in self.vertices)
        return f"polygon({vertices_repr})"
    
    def __eq__(self, other):
        '''Check to see if two polygons are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if len(self.vertices) != len(other.vertices):
            return False
        sorted_vertices1 = sorted(self.vertices, key=lambda vertex: (vertex.x, vertex.y))
        sorted_vertices2 = sorted(other.vertices, key=lambda vertex: (vertex.x, vertex.y))
        return sorted_vertices1 == sorted_vertices2


#___Three-Dimensional (3D) Geometric Shapes___
class shape3d(object):
    '''Generic base class for three-dimensional shapes.'''

    def __init__(self):
        pass

    def volume(self):
        '''Calculate the volume of the shape.'''
        raise NotImplementedError('volume() must be implemented by subclasses')
    
    def surfacearea(self):
        '''Calculate the surface area of the shape.'''
        raise NotImplementedError('surfacearea() must be implemented by subclasses')
    
    def contains(self, point):
        '''Return True if the point is inside the shape, False otherwise.'''
        raise NotImplementedError('contains() must be implemented by subclasses')
    
    def translate(self, dx, dy):
        '''Move the shape by a given displacement.'''
        raise NotImplementedError('translate() must be implemented by subclasses')
    
    def scale(self, factor):
        '''Scale the shape by a given factor.'''
        raise NotImplementedError('scale() must be implemented by subclasses')
    
    def iscongruent(self, other):
        '''Check to see if two shapes are congruent (same size and shape).'''
        raise NotImplementedError('iscongruent() must be implemented by subclasses')
    
    def __str__(self):
        '''A string representation of the shape.'''
        return '3D Shape'
    
    def __repr__(self):
        return 'shape3d()'
    
    def __eq__(self, other):
        '''Check to see if two shapes are equal.'''
        if self is other:
            return True
        if isinstance(other, shape3d):
            return True
        return False
    
class rectangularprism(shape3d):
    '''Represents a rectanglular prism in a three-dimensional space. Can also
    represent a cube if the width, and height, and depth are equal.'''

    def __init__(self, width, height, depth, bottom_left_back=None):
        if bottom_left_back is not None:
            if not isinstance(bottom_left_back, point):
                raise TypeError('bottom_left must be of type \'point\'')
            if not bottom_left_back.is3d():
                raise ValueError('bottom_left_back must be in 3D space')
        self.width = width
        self.height = height
        self.depth = depth
        self.bottom_left_back = bottom_left_back

    def volume(self):
        '''Calculate the volume of the rectangular prism.'''
        return self.width * self.height * self.depth
    
    def surfacearea(self):
        '''Calculate the surface area of the rectangular prism.'''
        return 2 * (self.width * self.height + self.width * self.depth + self.height * self.depth)
    
    def contains(self, point):
        '''Return True if the point is inside the rectangular prism, False
        otherwise.'''
        if self.bottom_left_back is None:
            raise ValueError('bottom_left must be defined to check containment')
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if not point.is3d():
            raise ValueError('point must be in 3D space')    
        return (self.bottom_left_back.x <= point.x <= self.bottom_left_back.x + self.width and
                self.bottom_left_back.y <= point.y <= self.bottom_left_back.y + self.height and
                self.bottom_left_back.z <= point.z <= self.bottom_left_back.z + self.depth)
    
    def translate(self, dx, dy, dz):
        '''Move the rectanglular prism by a given displacement.'''
        if self.bottom_left_back is not None:
            self.bottom_left_back.translate(dx, dy, dz)
    
    def scale(self, factor):
        '''Scale the rectanglular prism by a given factor.'''   
        self.width *= factor
        self.height *= factor
        self.depth *= factor
        if self.bottom_left_back is not None:
            self.bottom_left_back.scale(factor)
    
    def iscongruent(self, other):
        '''Check to see if two rectanglular prisms are congruent (same width,
        height, and depth).'''
        if not isinstance(other, rectangularprism):
            raise TypeError('other must be a rectanglular prism')
        return (self.width == other.width and self.height == other.height and self.depth == other.depth) or \
               (self.width == other.width and self.height == other.depth and self.depth == other.height) or \
               (self.width == other.depth and self.height == other.width and self.depth == other.height)
    
    def iscube(self):
        '''Check to see if the rectangular prism is a cube.'''
        return self.width == self.height == self.depth
    
    def __str__(self):
        '''A string representation of the rectangular prism.'''
        if self.bottom_left_back is not None:
            if self.iscube():
                return f'Cube with side length {self.width}, and bottom-left-back corner at {self.bottom_left_back}'
            else:
                return f'Rectangular prism with width {self.width}, height {self.height}, depth {self.depth}, and bottom-left-back corner at {self.bottom_left_back}'
        else:
            if self.iscube():
                return f'Cube with side length {self.width}'
            else:
                return f'Rectangular prism with width {self.width}, height {self.height}, and depth {self.depth}'

    def __repr__(self):
        if self.bottom_left_back is not None:
            return f'rectangular_prism({self.width}, {self.height}, {self.depth}, {repr(self.bottom_left_back)})'
        else:
            return f'rectangular_prism({self.width}, {self.height}, {self.depth})'
        
    def __eq__(self, other):
        '''Check to see if two rectangular prisms are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return (self.width == other.width and 
                self.height == other.height and 
                self.depth == other.depth and 
                self.bottom_left_back == other.bottom_left_back)

class sphere(shape3d):
    '''Represents a sphere in three-dimensional space.'''

    def __init__(self, radius, center = None):
        if center is not None:
            if not isinstance(center, point):
                raise TypeError('center must be of type \'point\'')
            if not center.is3d():
                raise ValueError('center must be in 3D space')
        self.radius = radius
        self.center = center

    def diameter(self):
        '''Calculate the diameter of the sphere.'''
        return self.radius * 2
    
    def circumference(self):
        '''Calculate the circumference of the sphere.'''
        return 2 * PI * self.radius
    
    def volume(self):
        '''Calculate the volume of the sphere.'''
        return (4 / 3) * PI * pow(self.radius, 3)
    
    def surfacearea(self):
        '''Calculate the surface area of the sphere.'''
        return (4 * PI) * pow(self.radius, 2)
    
    def contains(self, point):
        '''Return True if the point is inside the sphere, False otherwise.'''
        if not isinstance(point, point):
            raise TypeError('point must be of type \'point\'')
        if not point.is3d():
            raise ValueError('point must be in 3D space')
        return self.center.distance(point) <= self.radius
    
    def translate(self, dx, dy, dz):
        '''Move the sphere by a given displacement.'''
        if self.center is not None:
            self.center.translate(dx, dy, dz)    

    def scale(self, factor):
        '''Scale the sphere by a given factor.'''
        self.radius *= factor
        if self.center is not None:
            self.center.scale(factor)
    
    def iscongruent(self, other):
        '''Check to see if two spheres are congruent (same radius).'''
        if not isinstance(other, sphere):
            raise TypeError('other must be a sphere')
        return self.radius == other.radius

    def __str__(self):
        '''A string representation of the sphere.'''
        if self.center is not None:
            return f'Sphere with radius {self.radius}, and center at {self.center}'
        else:
            return f'Sphere with radius {self.radius}'

    def __repr__(self):
        if self.center is not None:
            return f'sphere({self.radius}, {repr(self.center)})'
        else:
             return f'sphere({self.radius})'
        
    def __eq__(self, other):
        '''Check to see if two spheres are equal.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.radius == other.radius and self.center == other.center