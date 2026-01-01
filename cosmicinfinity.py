'''Cosmic Core: Cosmic Infinity
\n\tA module containing data types and functions for infinite numbers and sets.'''
from .cosmicdatastructures import *
from .cosmicmath import *
from numpy import ndarray
__all__ = ['aleph', 'beth', 'ordinal', 'toordinal', 'countableset',
           'uncountableset', 'NATURAL_NUMBERS', 'REAL_NUMBERS', 'cardinality',
           'isinfinite']


#___Transfinite Number Data Types___
class aleph(object):
    '''Represents an Aleph number (transfinite cardinal).'''

    def __init__(self, index):
        if not isinstance(index, (int, ordinal)):
            raise TypeError('index must be an integer or ordinal')
        if index < 0:
            raise ValueError('index must be non-negative')
        self.index = index
    
    def __str__(self):
        '''Return the string representation of the Aleph number.'''
        if isinstance(self.index, ordinal):
            return f'ℵ({self.index})'
        if isinstance(self.index, int):
            return f'ℵ{self.index}'
    
    def __repr__(self):
        return f'aleph({self.index})'
    
    def __eq__(self, other):
        '''Compare two Aleph numbers to see if they are equal.'''
        if self is other:
            return True
        if self.index == 0:
            if isinstance(other, ordinal):
                return True
            if isinstance(other, beth) and other.index == 0:
                return True
        if not isinstance(other, aleph):
            return False
        return self.index == other.index
    
    def __ne__(self, other):
        '''Not equal to comparison.'''
        return not self.__eq__(other)     
    
    def __lt__(self, other):
        '''Less than comparison.'''
        if not isinstance(other, (int, float, aleph, beth, ordinal)):
            raise TypeError('can only compare aleph numbers to ints, floats numbers, aleph numbers, beth numbers, and ordinals')
        if isinstance(other, (int, float)):
            return False
        if isinstance(other, ordinal):
            if self.index >= 1:
                return False
        if isinstance(other, beth):
            if other.index > 0:
                return True
            elif self.index > 0:
                return False
        return self.index < other.index
    
    def __le__(self, other):
        '''Less than or equal to comparison'''
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        '''Greater than comparison.'''
        return not self.__le__(other)
    
    def __ge__(self, other):
        '''Greater than or equal to comparison.'''
        return not self.__lt__(other)
    
    def __add__(self, other):
        '''Add two Aleph numbers.'''
        if isinstance(other, (int, float)):
            return self
        if not isinstance(other, int, float, aleph, beth):
            raise TypeError('can only add ints, floats numbers, aleph numbers, and beth numbers to aleph numbers')
        if self.index == other.index:
            return aleph(self.index)
        elif self.index > other.index:
            return aleph(self.index)
        else:
            return aleph(other.index)

    def __mul__(self, other):
        '''Multiply two Aleph numbers.'''
        if not isinstance(other, aleph, beth):
            raise TypeError('can only multiply aleph numbers and beth numbers to aleph numbers')
        if self.index == 0 or other.index == 0:
            return type(other)(0)
        else:
            return type(other)(max(self.index, other.index))
        
    def __rpow__(self, other):
        if other == 1:
            return 1
        if other >= 2 and self.index == 0:
            return beth(1)
        
class beth(object):
    '''Represents an Beth number (transfinite cardinal defined as ℶ0 = ℵ0 and ℶn+1 = 2^ℶn).'''

    def __init__(self, index):
        if not isinstance(index, (int, ordinal)):
            raise TypeError('index must be an integer or ordinal')
        if index < 0:
            raise ValueError('index must be non-negative')
        self.index = index
    
    def __str__(self):
        '''Return the string representation of the Beth number.'''
        if isinstance(self.index, ordinal):
            return f'ℶ({self.index})'
        if isinstance(self.index, int):
            return f'ℶ{self.index}'
    
    def __repr__(self):
        return f'beth({self.index})'
    
    def __eq__(self, other):
        '''Compare two Beth numbers to see if they are equal.'''
        if self is other:
            return True
        if self.index == 0:
            if isinstance(other, ordinal):
                return True
            if isinstance(other, beth) and other.index == 0:
                return True
        if not isinstance(other, beth):
            return False
        return self.index == other.index
    
    def __ne__(self, other):
        '''Not equal to comparison.'''
        return not self.__eq__(other)
    
    def __lt__(self, other):
        '''Less than comparison.'''
        if not isinstance(other, (int, float, aleph, beth, ordinal)):
            raise TypeError('can only compare beth numbers to ints, floats numbers, aleph numbers, beth numbers, and ordinals')
        if isinstance(other, (int, float)):
            return False
        if isinstance(other, ordinal):
            if self.index >= 1:
                return False
        if isinstance(other, aleph):
            if self.index > 0:
                return False
            elif other.index > 0:
                return True
        return self.index < other.index
    
    def __le__(self, other):
        '''Less than or equal to comparison'''
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        '''Greater than comparison.'''
        return not self.__le__(other)
    
    def __ge__(self, other):
        '''Greater than or equal to comparison.'''
        return not self.__lt__(other)
    
    def __add__(self, other):
        '''Add two Beth numbers.'''
        if isinstance(other, (int, float)):
            return self
        if not isinstance(other, int, float, aleph, beth):
            raise TypeError('can only add ints, floats numbers, aleph numbers, and beth numbers to aleph numbers')
        if self.index == other.index:
            return aleph(self.index)
        elif self.index > other.index:
            return aleph(self.index)
        else:
            return aleph(other.index)

    def __mul__(self, other):
        '''Multiply two Beth numbers.'''
        if not isinstance(other, aleph, beth):
            raise TypeError('can only multiply aleph numbers and beth numbers to beth numbers')
        if self.index == 0 or other.index == 0:
            return type(other)(0)
        else:
            return type(other)(max(self.index, other.index))
        
    def __rpow__(self, other):
        if other == 1:
            return 1
        if other >= 2:
            return beth(self.index + 1)

class ordinal:
    '''Represents an ordinal number using nested lists. For example, 
    ordinal([[1, 5], [0, 2]]) represents 5ω + 2. Lists can be nested to
    represent larger ordinals. For instance, ordinal([[[1, 1], 1]]) represents ω^ω. 
    The theoretical upper bound of representable values with this data type is
    ω tetrated to ω, aka ε0.'''

    def __init__(self, coefficients = [[0, 0]]):
        if not isinstance(coefficients, list):
            raise TypeError('coefficients must be a list')
        if not all(isinstance(item, list) for item in coefficients):
            raise TypeError('elements of coefficients list must be lists')
        if not all(len(item) == 2 for item in coefficients):
            raise ValueError('each element of coefficients list must have exactly two elements')
        if not all(isinstance(item[0], (int, list)) for item in coefficients):
            raise TypeError('first element of each inner list must be an integer or list')
        if not all(isinstance(item[1], (int)) for item in coefficients):
            raise TypeError('second element of each inner list must be an integer')
        #Sort coefficients by exponent in descending order
        def compare_exponents(item):
            if isinstance(item[0], list):
                return item[0]
            else:
                return item[0]  #Integers are already comparable

        self.coefficients = sorted(coefficients, key=compare_exponents, reverse=True)

    def __str__(self):
        '''Return a string representation of the ordinal.'''
        terms = []
        for exponent, coeff in self.coefficients:
            if coeff != 0:
                if exponent == 0:
                    terms.append(str(coeff))
                elif exponent == 1:
                    if coeff == 1:
                        terms.append('ω')
                    else:
                        terms.append(f'{coeff}ω')
                else:
                    if coeff == 1:
                        if isinstance(exponent, list):
                            terms.append(f'ω^{ordinal([exponent])}')  # Recursive call for ordinal exponents
                        else:
                            terms.append(f'ω^{exponent}')
                    else:
                        if isinstance(exponent, list):
                            terms.append(f'{coeff}ω^{ordinal([exponent])}')  # Recursive call for ordinal exponents
                        else:
                            terms.append(f'{coeff}ω^{exponent}')
        if not terms:
            return '0'
        return ' + '.join(terms).replace('+ -', '- ')

    def __repr__(self):
        return f'ordinal({self.coefficients})'

    def __eq__(self, other):
        '''Check if two ordinals are equal.'''
        if self is other:
            return True
        if not isinstance(other, (ordinal, int, float)):
            return False
        if isinstance(other, (int, float)):
            if len(self.coefficients) > 1:
                return False
            else:
                if 0 in self.coefficients:
                    return self.coefficients[0][1] == other
                else:
                    return False
        return self.coefficients == other.coefficients

    def __ne__(self, other):
        '''Not equal to comparison.'''
        return not self.__eq__(other)

    def __lt__(self, other):
        '''Less than comparison.'''
        if not isinstance(other, (ordinal, int, float)):
            raise TypeError('can only compare ordinals to ints, floats numbers, and ordinals')
        if isinstance(other, (int, float)):
            if len(self.coefficients) > 1:
                return False
            else:
                if 0 in self.coefficients:
                    return self.coefficients[0][1] < other
                else:
                    return False
        for i in range(max(len(self.coefficients), len(other.coefficients))):
            self_coeff = self.coefficients[i][1] if i < len(self.coefficients) else 0
            other_coeff = other.coefficients[i][1] if i < len(other.coefficients) else 0
            if self_coeff < other_coeff:
                return True
            elif self_coeff > other_coeff:
                return False
        return False

    def __le__(self, other):
        '''Less than or equal to comparison'''
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        '''Greater than comparison.'''
        return not self.__le__(other)

    def __ge__(self, other):
        '''Greater than or equal to comparison.'''
        return not self.__lt__(other)

    def __add__(self, other):
        '''Add two ordinals.'''
        if not isinstance(other, (int, ordinal)):
            raise TypeError('can only add ordinals and ints to ordinals')
        if isinstance(other, (int)):
            other = toordinal(other)
        result_coefficients = self.coefficients.copy()
        for exponent, coefficient in other.coefficients:
            found = False
            for i, (result_exponent, result_coefficient) in enumerate(result_coefficients):
                if result_exponent == exponent:
                    result_coefficients[i] = [exponent, result_coefficient + coefficient]
                    found = True
                    break
            if not found:
                result_coefficients.append([exponent, coefficient])
        return ordinal(result_coefficients)
    
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return self
        else:
            return self.__add__(other)

    def __mul__(self, other):
        '''Multiply two ordinals.'''
        if not isinstance(other, ordinal):
            raise TypeError('can only multiply ordinals by other ordinals')
        if other == 0:
            return 0
        if self == 0:
            return 0
        result_coefficients = []
        for exponent, coefficient in self.coefficients:
            for other_exponent, other_coefficient in other.coefficients:
                result_exponent = exponent + other_exponent
                result_coefficient = coefficient * other_coefficient
                found = False
                for i, (result_exponent2, result_coefficient2) in enumerate(result_coefficients):
                    if result_exponent2 == result_exponent:
                        result_coefficients[i] = [result_exponent, result_coefficient2 + result_coefficient]
                        found = True
                        break
                if not found:
                    result_coefficients.append([result_exponent, result_coefficient])
        return ordinal(result_coefficients)

    def __pow__(self, other):
        '''Raise an ordinal to a power. Only supported for powers of omega.'''
        if not isinstance(other, int):
            raise TypeError('exponent must be an integer')
        if other == 0:
            return 1
        if other < 0:
            raise ValueError('negative exponents are not supported for ordinals')
        if other == 1:
            return self
        result = self
        for i in range(1, other):
            result *= self
        return result

def toordinal(x):
    '''Convert an int to an ordinal.'''
    if not isinstance(x, (int)):
        raise TypeError('can only convert ints to ordinals')
    return ordinal([[0, x]])


#___Set Theory___
class countableset(object):
    '''Represents a countably infinite (denumerable) set.'''

    def __init__(self, start=0, increment=1):
        self.start = start
        self.increment = increment

    def __iter__(self, max_iterations = None):
        '''Iterates through the set.'''
        if self.increment == None:
            raise TypeError('increment must be defined in order to iterate')
        item = self.start
        iteration_count = 0
        while max_iterations is None or iteration_count < max_iterations:
            yield item
            item += self.increment
            iteration_count += 1

    def __str__(self):
        '''Return a string representation of the set.'''
        return f'Countably infinite set: {{{self.start}, {self.start + self.increment}, {self.start + (2 * self.increment)}, ...}}'

    def __repr__(self):
        return f'countableset({self.start}, {self.increment})'

class uncountableset(object):
    '''Represents an uncountably infinite set.'''

    def __init__(self, definition = None, cardinality = aleph(1)):
        self.definition = definition
        if isinstance(cardinality, (int, float)):
            raise TypeError('uncountable sets cannot have finite cardinality')
        elif isinstance(cardinality, (aleph, beth)):
            if cardinality == aleph(0) or cardinality == beth(0):
                raise ValueError('uncountable sets must have cardinality greater than aleph 0')
            self.cardinality = cardinality
        else:
            raise TypeError('invalid data type for cardinality')

    def __str__(self):
        '''Return a string representation of the set.'''
        if self.definition is None:
            return f'Uncountably infinite set with cardinality {self.cardinality}'
        else:
            return f'Uncountably infinite set containing {self.definition.lower()} (Cardinality: {self.cardinality})'
        
    def __repr__(self):
        if self.definition is None:
            return 'uncountableset()'
        else:
            return f'uncountableset({self.definition}, {self.cardinality})'
        
NATURAL_NUMBERS = countableset(0, 1)
REAL_NUMBERS = uncountableset('all real numbers', beth(1)) 
#The cardinality of the set of all real numbers is 2^ℵ0, equivalent to ℶ1.
#The theory that states 2^ℵ0 = ℵ1 is called the Continuum Hypothesis, which
#would also imply a 1-to-1 correspondence between the Aleph numbers and the Beth
#numbers. Since the Continuum Hypothesis is unproven, the cardinality of
#REAL_NUMBERS is defined as ℶ1, which, given the definition of the Beth numbers,
#is true regardless of whether or not the Continuum Hypothesis is true.

def cardinality(data):
    '''Return the cardinality of a data set.'''
    if isinstance(data, (list, linklist, dlinklist, set)):
        return len(data)
    if isinstance(data, ndarray):
        return data.size
    elif isinstance(data, countableset):
        return aleph(0)
    elif isinstance(data, uncountableset):
        return data.cardinality
    else:
        raise TypeError('invalid data type')
    

#__Classification Functions__
def isinfinite(x):
    '''Return True if x is positive or negative infinity, an aleph number,
     a beth number, or a transfinite ordinal, and False otherwise.'''
    if isinstance(x, (aleph, beth)):
        return True
    if isinstance(x, ordinal):
        return any(exponent != 0 for exponent, _ in x.coefficients) 
    return isinf(x)