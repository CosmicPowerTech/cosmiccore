'''Cosmic Core: Cosmic Math
\n\tAn upgrade of the built-in math and cmath modules that alternates between real and complex numbers, and also contains new classes and functions.'''
import math
import cmath
__all__ = ['PHI', 'E', 'PI', 'TAU', 'AVOGADROS_NUMBER', 'ceil', 'comb',
           'copysign', 'fabs', 'factorial', 'floor', 'fmod', 'frexp',
           'fsum', 'gcd', 'isqrt', 'lcm', 'ldexp', 'modf', 'nextafter',
           'perm', 'prod', 'remainder', 'trunc', 'ulp', 'phase', 'polar',
           'rect', 'log', 'root', 'sqrt', 'cbrt', 'log2', 'log1p', 'acos',
           'asin', 'atan', 'cos', 'sin', 'tan', 'atan2', 'dist', 'hypot',
           'degrees', 'radians', 'acosh', 'asinh', 'atanh', 'cosh', 'sinh',
           'tanh', 'erf', 'erfc', 'gamma', 'lgamma', 'isclose', 'iseven',
           'isfinite', 'isinf', 'isnan', 'isprime', 'average', 'fibonacci',
           'fibonaccilist', 'primefactorization', 'tetration', 'inf','infj',
           'nan', 'nanj']

#___Numerical Constants___
from cmath import inf, infj, nan, nanj

PHI = (math.sqrt(5) + 1) / 2 #The Golden Ratio, also known as phi.
E = 2.7182818284590452353602874713526624977572470936999 #E to 50 digits.
PI = 3.1415926535897932384626433832795028841971693993751 #Pi to 50 digits.
TAU = 6.2831853071795864769252867665590057683943387987502 #Tau to 50 digits.
AVOGADROS_NUMBER = (6.02214076) * pow(10, 23) #Avogadro's number.


#___Number-Theoretic and Representation Functions___
#Since none of these functions exist in cmath, they're imported from math.
from math import (ceil, comb, copysign, fabs, factorial, floor, fmod, frexp, 
                  fsum, gcd, isqrt, lcm, ldexp, modf, nextafter, perm, prod,
                  remainder, trunc, ulp)


#___Conversions to and from Polar Coordinates___
#Since none of these functions exist in math, they're imported from cmath.
from cmath import phase, polar, rect


#___Power and Logarithmic Functions___
from math import log2, log1p

def log(x, y = E):
    '''Return the logarithm of x to the given base.\n
    If the base is not specified, returns the natural logarithm (base e) of x.'''

    try:
        return math.log(x, y)
    except (ValueError, TypeError):
        return cmath.log(x, y)
    
def root(x, y):
    '''Return the yth root of x.'''
    return pow(x, 1.0/y)

def sqrt(x):
    '''Return the square root of x.'''
    try:
        return math.sqrt(x)
    except (ValueError, TypeError):
        return cmath.sqrt(x)
    
def cbrt(x):
    '''Return the cube root root of x.'''
    return pow(x, 1.0/3.0)

#___Triginometric Functions___
from math import atan2, dist, hypot

def acos(x):
    '''Return the arc cosine (measured in radians) of x.\n
    The result is between 0 and pi.'''
    try:
        return math.acos(x)
    except (ValueError, TypeError):
        return cmath.acos(x)
    
def asin(x):
    '''Return the arc sine (measured in radians) of x.\n
    The result is between -pi/2 and pi/2.'''
    try:
        return math.asin(x)
    except (ValueError, TypeError):
        return cmath.asin(x)
    
def atan(x):
    '''Return the arc tangent (measured in radians) of x.\n
    The result is between -pi/2 and pi/2.'''    
    try:
        return math.atan(x)
    except (ValueError, TypeError):
        return cmath.atan(x)

def cos(x):
    '''Return the cosine of x (measured in radians).'''
    try:
        return math.cos(x)
    except (ValueError, TypeError):
        return cmath.cos(x)
    
def sin(x):
    '''Return the sine of x (measured in radians).'''
    try:
        return math.sin(x)
    except (ValueError, TypeError):
        return cmath.sin(x)
    
def tan(x):
    '''Return the tangent of x (measured in radians).'''
    try:
        return math.tan(x)
    except (ValueError, TypeError):
        return cmath.tan(x)


#___Angular Conversion Functions___
#Since neither of these functions exist in cmath, they're imported from math.
from math import degrees, radians


#___Hyperbolic Functions___
def acosh(x):
    '''Return the inverse hyperbolic cosine of x.'''
    try:
        return math.acosh(x)
    except (ValueError, TypeError):
        return cmath.acosh(x)
    
def asinh(x):
    '''Return the inverse hyperbolic sine of x.'''
    try:
        return math.asinh(x)
    except (ValueError, TypeError):
        return cmath.asinh(x)
    
def atanh(x):
    '''Return the inverse hyperbolic tangent of x.'''    
    try:
        return math.atanh(x)
    except (ValueError, TypeError):
        return cmath.atanh(x)

def cosh(x):
    '''Return the hyperbolic cosine of x..'''
    try:
        return math.cosh(x)
    except (ValueError, TypeError):
        return cmath.cosh(x)
    
def sinh(x):
    '''Return the hyperbolic sine of x.'''
    try:
        return math.sinh(x)
    except (ValueError, TypeError):
        return cmath.sinh(x)
    
def tanh(x):
    '''Return the hyperbolic tangent of x.'''
    try:
        return math.tanh(x)
    except (ValueError, TypeError):
        return cmath.tanh(x)
    

#___Special Functions___
#Since none of these functions exist in cmath, they're imported from math.
from math import erf, erfc, gamma, lgamma


#___Classification Functions___
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''Determine whether two floating point or complex numbers are close in value.\n
    rel_tol\n\tmaximum difference for being considered "close", relative to the magnitude of the input values
    abs_tol\n\tmaximum difference for being considered "close", regardless of the magnitude of the input values'''
    if type(a) == complex or type(b) == complex:
        return cmath.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
    else:
        return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
    
def iseven(x):
    '''Return True if x is even, False otherwise.'''
    if not isinstance(x, int):
        raise TypeError('input must be an integer')
    return x % 2 == 0

def isfinite(x):
    '''Return True if x is not an infinity or a NaN and False otherwise.'''
    if isinstance(x, complex):
        return cmath.isfinite(x)
    else:
        return math.isfinite(x)

def isinf(x):
    '''Return True if x is a positive or negative infinity, and False otherwise.'''
    if isinstance(x, complex):
        return cmath.isinf(x)
    else:
        return math.isinf(x)

def isnan(x):
    '''Return True if x is NaN (not a number), and False otherwise.'''
    if isinstance(x, complex):
        return cmath.isnan(x)
    else:
        return math.isnan(x)
    
def isprime(x):
    '''Determine if x is prime.
    \nPrecondition: x is an integer.'''
    if not isinstance(x, int):
        raise TypeError('input must be an integer')
    if x <= 1:
        return False
    for i in range (2, x):
        if x % i == 0:
            return False
    return True


#___Statistical Functions___
def average(nums):
    '''Find the average of any iterable filled with numbers.'''
    if len(nums) == 0:
        return 0
    return sum(nums) / len(nums)

def variance(data):
    '''Calculate the variance of a dataset.
    \nPrecondition: data is an iterable of numbers.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    if len(data) == 0:
        raise ValueError('data must not be empty')

    mean = sum(data) / len(data)
    return sum((x - mean) ** 2 for x in data) / len(data)

def standarddeviation(data):
    '''Calculate the standard deviation of a dataset.
    \nPrecondition: data is an iterable of numbers.'''
    return sqrt(variance(data))


#___Number Theory Functions___
def fibonacci(n):
    '''Find the nth number in the Fibonacci sequence.
        \nPrecondition: x is an integer.'''
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    num = 0
    if n != 0:
      num = 1
      lastnum = 0
      for i in range (1, abs(n)):
          tempnum = num
          num += lastnum
          lastnum = tempnum
      if n < 0 and n % 2 == 0:
        num *= -1
    else:
      num = 0
    return num

def fibonaccilist(n):
    '''Generate a list containing the first n Fibonacci numbers.
    \nPrecondition: x is a non-negative integer.'''
    if not isinstance(n, int):
        raise TypeError('n must be an integer')
    if n < 0:
        raise ValueError('n must be greater than 0')
    fib_list = []
    a, b = 0, 1
    for i in range(n):
        fib_list.append(a)
        a, b = b, a + b
    return fib_list

def primefactorization(n):
    '''Return a list of prime factors of a positive integer.'''
    if not isinstance(n, int):
        raise TypeError('input must be an integer')
    if n <= 0:
        raise ValueError('input must be a positive integer')

    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1

    if n > 1:
        factors.append(n)

    return factors


#___Hyperoperations___
def tetration(x, y):
    '''Return x raised to the power of itself y times (or x tetrated to y).
    \nPrecondition: y is an integer.'''
    result = 1
    if y % 1 != 0:
        raise TypeError('tetration for non-integer heights is not yet implemented')
    for i in range(y):
        result = pow(x, result)
    return result