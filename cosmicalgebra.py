'''Cosmic Core: Cosmic Algebra
\n\tA module containing data types and functions for various algebraic fields.'''
import numpy
from numpy import array, ndarray
from .cosmicdatastructures import *
from .cosmicinfinity import *
from .cosmicmath import *
__all__ = ['quadraticformula', 'polynomial', 'matrix']

#___Finding Zeroes___
def quadraticformula(a, b, c):
    '''Find the zeroes of a quadratic function.'''
    zeroes = [nan, nan]
    zeroes[0] = (((b * -1) + sqrt(pow(b, 2) - (4 * a * c))) / (2 * a))
    zeroes[1] = (((b * -1) - sqrt(pow(b, 2) - (4 * a * c))) / (2 * a))
    return zeroes

#__Polynomials
class polynomial(object):
    '''Represents a univariate polynomial via list, with each index
    representing the power of the variable x. \n
    For instance, index 0 represents the constant, index 1 represents the
    coefficient of x, index 2 represents the coefficient of x^2, and so on.'''

    def __init__(self, coefficients):
        if not isinstance(coefficients, (ndarray, list, linklist, dlinklist)):
            raise TypeError('coefficients must be a list, linked list, or NumPy array')
        self.coefficients = coefficients

    def degree(self):
        '''Return the degree of the polynomial.'''
        return len(self.coefficients) - 1
    
    def evaluate(self, x):
        '''Evaluate the polynomial at a given value of x.'''
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * x**i
        return result

    def zeroes(self):
        '''Return all the zeroes of the polynomial.'''
        if self.degree() == 0: #Constant
            if self.coefficients[0] == 0:
                return REAL_NUMBERS
            else:
                return []
        elif self.degree() == 1: #Linear polynomial
            return [(self.coefficients[0] * -1) / self.coefficients[1]]
        elif self.degree() == 2: #Quadratic polynomial
            return quadraticformula(self.coefficients[2], self.coefficients[1],
                                    self.coefficients[0])
        else: #Higher degree polynomial
            return numpy.roots(self.coefficients).tolist()
        
    def derivative(self):
        '''Return the derivative of the polynomial.'''
        if self.degree() == 0:  #Derivative of a constant is 0
            return polynomial([0])
        else:
            #Calculate the derivative's coefficients
            derivative_coefficients = [
                self.coefficients[i] * i
                for i in range(1, len(self.coefficients))
            ]
            return polynomial(derivative_coefficients)

    def __str__(self):
        '''Return a string representation of the polynomial.'''
        terms = []
        for i, coeff in enumerate(self.coefficients):
            if coeff != 0:
                if i == 0:
                    terms.insert(0, f'{coeff}')
                elif i == 1:
                    if coeff == 1:
                        terms.insert(0, 'x')
                    else:
                        terms.insert(0, f'{coeff}x')
                else:
                    if coeff == 1:
                        terms.insert(0, f'x^{i}')
                    else:
                        terms.insert(0, f'{coeff}x^{i}')
        if not terms:
            return '0'
        return ' + '.join(terms).replace('+ -', '- ')
    
    def __repr__(self):
        return f'polynomial({self.coefficients})'
    
    def __add__(self, other):
        '''Add two polynomials.'''
        if not isinstance(other, polynomial):
            raise TypeError('can only add polynomials to polynomials')
        max_degree = max(self.degree(), other.degree())
        result_coefficients = [0] * (max_degree + 1)
        for i in range(self.degree() + 1):
            result_coefficients[i] += self.coefficients[i]
        for i in range(other.degree() + 1):
            result_coefficients[i] += other.coefficients[i]
        return polynomial(result_coefficients)

    def __sub__(self, other):
        '''Subtract two polynomials.'''
        if not isinstance(other, polynomial):
            raise TypeError('can only subtract polynomials from polynomials')
        max_degree = max(self.degree(), other.degree())
        result_coefficients = [0] * (max_degree + 1)
        for i in range(self.degree() + 1):
            result_coefficients[i] += self.coefficients[i]
        for i in range(other.degree() + 1):
            result_coefficients[i] -= other.coefficients[i]
        return polynomial(result_coefficients)

    def __mul__(self, other):
        '''Multiplie two polynomials.'''
        if not isinstance(other, polynomial):
            raise TypeError('can only multiply polynomials by polynomials')
        result_coefficients = [0] * (self.degree() + other.degree() + 1)
        for i in range(self.degree() + 1):
            for j in range(other.degree() + 1):
                result_coefficients[i + j] += self.coefficients[i] * other.coefficients[j]
        return polynomial(result_coefficients)

    def __neg__(self):
        '''Return the negation of the polynomial.'''
        return polynomial([-c for c in self.coefficients])


#___Matrices and Linear Algebra
class matrix(object):
    '''Represents a mathematical matrix.'''
    def __init__(self, data):
        if isinstance(data, (list, linklist, dlinklist)):
            if not all(isinstance(row, (list, linklist, dlinklist, ndarray)) for row in data):
                raise TypeError('all elements in data must be lists, linked lists, or NumPy arrays')
            if len(data) == 0 or any(len(row) == 0 for row in data):
                raise ValueError('input data cannot be empty')
            self.data = array(data)
        elif isinstance(data, ndarray):
            if data.size == 0:
                raise ValueError('input data cannot be empty')
            self.data = data
        else:
            raise TypeError('data must be a list, linked list, or NumPy array')

    def __str__(self):
        '''Return a string representation of the matrix.'''
        return str(self.data)

    
    def __repr__(self):
        return f'matrix({self.data})'
    
    def isrow(self):
        '''Return True if the matrix is a row vector, and False otherwise.'''
        return self.data.shape[0] == 1
    
    def iscolumn(self):
        '''Return True if the matrix is a column vector, and False otherwise.'''
        return self.data.shape[1] == 1
    
    def issquare(self):
        '''Return True if the matrix is a square matrix, and False otherwise.'''
        return self.data.shape[0] == self.data.shape[1]
    
    def hassamedimensions(self, other):
        '''Return True if the two matrices have the same dimensions, and False otherwise.'''
        return self.data.shape == other.data.shape
    
    def __eq__(self, other):
        '''Return True if two matrices are equal, and False otherwise.'''
        if self is other:
            return True
        if not isinstance(other, matrix):
            return False
        return numpy.array_equal(self.data, other.data)
    
    def copy(self):
        '''Return a deep copy of the matrix.'''
        return matrix(self.data.copy())
    
    def __add__(self, other):
        '''Matrix addition.'''
        if not isinstance(other, matrix):
            raise TypeError('can only add matrices to other matrices')
        if not self.hassamedimensions(other):
            raise ValueError('matrices must have the same dimensions for addition')
        return matrix(self.data + other.data)
    
    def __sub__(self, other):
        '''Matrix subtraction.'''
        if not isinstance(other, matrix):
            raise TypeError('can only subtract matrices from other matrices')
        if not self.hassamedimensions(other):
            raise ValueError('matrices must have the same dimensions for subtraction')
        return matrix(self.data - other.data)
    
    def __mul__(self, other):
        if isinstance(other, matrix):
            #Matrix multiplication
            if self.data.shape[1] != other.data.shape[0] or \
            other.data.shape[1] != self.data.shape[0]:
                raise ValueError('number of columns in the first matrix must equal the number of rows in the second matrix')
            return matrix(self.data @ other.data)
        elif isinstance(other, (int, float)):
            #Scalar multiplication
            return matrix(self.data * other)
        elif isinstance(other, (list, linklist, dlinklist)):
            #Matrix multiplication by vector
            if self.data.shape[1] != len(other):
                raise ValueError('number of columns in the matrix must match the length of the vector')
            return matrix(self.data @ array(other))
        else:
            raise TypeError('can only multiply matrices by other matrices, scalars, or vectors')
        
    def __rmul__(self, other):
        '''Right-hand multiplication.'''
        return self.__mul__(other)
    
    def __neg__(self):
        '''Return the negation of the matrix.'''
        return self * -1
    
    def swaprows(self, row1, row2):
        '''Swap two rows in the matrix.'''
        if row1 < 0 or row1 >= len(self.data) or row2 < 0 or row2 >= len(self.data):
            raise IndexError('invalid row indices')
        self.data[row1], self.data[row2] = self.data[row2], self.data[row1]

    def scalerow(self, row, factor):
        '''Multiply a row by a scalar.'''
        if row < 0 or row >= len(self.data):
            raise IndexError('invalid row index')
        self.data[row] = [factor * x for x in self.data[row]]

    def addrows(self, row1, row2, factor):
        '''Add a multiple of one row to another.'''
        if row1 < 0 or row1 >= len(self.data) or row2 < 0 or row2 >= len(self.data):
            raise IndexError('invalid row indices')
        self.data[row2] = [self.data[row2][i] + factor * self.data[row1][i] for i in range(len(self.data[0]))]

    def invert(self):
        '''Matrix inversion.'''
        if not self.issquare():
            raise ValueError('matrix must be square to be invertible')
        return matrix(numpy.linalg.inv(self.data))

    def determinant(self):
        '''Find the determinant of the matrix.'''
        if not self.issquare():
            raise ValueError('matrix must be square to calculate the determinant')
        return numpy.linalg.det(self.data)
    
    def transpose(self):
        '''Find the transpose of the matrix.'''
        return matrix(self.data.transpose())

    def eigen(self):
        '''Find the eigenvalues and eigenvectors of a matrix.'''
        if not self.issquare():
            raise ValueError('matrix must be square to calculate eigenvalues')
        eigenvalues, eigenvectors = numpy.linalg.eig(self.data)
        return eigenvalues, eigenvectors
    
    def dominanteigen(self):
        '''Find the dominant eigenvalue and eigenvector of a matrix.'''
        if not self.issquare():
            raise ValueError('matrix must be square to calculate eigenvalues')
        eigenvalues, eigenvectors = numpy.linalg.eig(self.data)
        dominant_index = numpy.argmax(numpy.abs(eigenvalues))
        dominant_eigenvalue = eigenvalues[dominant_index]
        dominant_eigenvector = eigenvectors[:, dominant_index]
        return dominant_eigenvalue, dominant_eigenvector
    
    def qrdecomposition(self):
        '''Decompose a matrix into an orthogonal matrix Q and an upper
        triangular matrix R.'''
        if not self.issquare():
            raise ValueError('matrix must be square to perform QR decomposition')
        Q, R = numpy.linalg.qr(self.data)
        return matrix(Q), matrix(R)
