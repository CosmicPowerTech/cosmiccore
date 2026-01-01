'''Cosmic Core: Cosmic Units
\n\tA library of data types and functions built to simplify use of units.'''
from .cosmicmath import *
__all__ = ['metric_prefixes', 'prefix_symbols', 'derived_dimensions', 'unit',
           'meter', 'plancklength', 'angstrom', 'inch', 'foot', 'yard', 'mile',
           'nauticalmile', 'astronomicalunit', 'lightyear', 'parsec',
           'temperature', 'celsius', 'fahrenheit', 'kelvin', 'second',
           'minute', 'hour', 'day', 'week', 'common_year', 'gram', 'ounce',
           'pound', 'tonne']


#___Metric Prefixes___
metric_prefixes = {'quecto' : pow(10, -30), 'ronto' : pow(10, -27),
                   'yocto' : pow(10, -24), 'zepto' : pow(10, -21), 
                   'atto' : pow(10, -18), 'femto' : pow(10, -15),
                   'pico' : pow(10, -12), 'nano' : pow(10, -9),
                   'micro' : 0.000001, 'milli' : 0.001, 'centi' : 0.01,
                   'deci' : 0.1, 'deca' : 10, 'hecto' : 100, 'kilo' : 1000, 
                   'mega' : 1000000, 'giga' : pow(10, 9), 'tera' : pow(10, 12), 
                   'peta' : pow(10, 15), 'exa' : pow(10, 18), 
                   'zetta' : pow(10, 21), 'yotta' : pow(10, 24),
                   'ronna' : pow(10, 27), 'quetta' : pow(10, 30)}
prefix_symbols = {'quecto' : 'q', 'ronto' : 'r', 'yocto' : 'y', 'zepto' : 'z',
                  'atto' : 'a', 'femto' : 'f', 'pico' : 'p', 'nano' : 'n',
                  'micro' : 'μ', 'milli' : 'm', 'centi' : 'c', 'deci' : 'd', 
                  'deca' : 'da', 'hecto' : 'h', 'kilo' : 'k', 'mega' : 'M',
                  'giga' : 'G', 'tera' : 'T', 'peta' : 'P', 'exa' : 'E', 
                  'zetta' : 'Z', 'yotta' : 'Y', 'ronna' : 'R', 'quetta' : 'Q'}
derived_dimensions = {'length * length' : 'area', 'length squared' : 'area', 
                      'length / time' : 'speed'}

#___Unit Base Class___
class unit(object):
    '''Generic base class for units.'''

    def __init__(self, name, symbol, dimension, base_unit = None, base_units_per_unit = 1.0, amount = 0.0, prefix = ''):
        self.name = name
        self.symbol = symbol
        self.dimension = dimension
        self.base_unit = base_unit
        self.base_units_per_unit = base_units_per_unit
        self.amount = amount
        self.prefix = prefix
        #Adjust the conversion factor if a prefix is applied
        if self.prefix is not None:
            self.base_units_per_unit *= metric_prefixes.get(self.prefix.lower(), 1)
        else:
            self.prefix = ''

    def convertprefix(self, new_prefix = ''):
        '''Change the metric prefix and adjusts the value accordingly.'''
        if new_prefix != '' and not new_prefix.lower() in metric_prefixes:
            raise ValueError('invalid prefix')
        new_factor = metric_prefixes.get(new_prefix.lower(), 1)
        self.amount /= new_factor * (1 / self.base_units_per_unit)
        self.prefix = new_prefix
        self.base_units_per_unit = new_factor

    def convert(self, target_unit):
        '''Convert from one unit to another.'''
        if not isinstance(target_unit, unit) or not issubclass(type(target_unit), unit):
            raise TypeError('target unit must be a unit')
        if target_unit.dimension != self.dimension:
            raise ValueError('target unit must have the same dimension as the original')
        conversion_factor = self.base_units_per_unit / target_unit.base_units_per_unit
        new_amount = self.amount * conversion_factor

        if type(target_unit) == unit:
            new_unit = unit(
                target_unit.name, target_unit.symbol, target_unit.dimension,
                target_unit.base_unit, target_unit.base_units_per_unit, 
                new_amount, target_unit.prefix)
        else:
            new_unit = type(target_unit)(new_amount, target_unit.prefix)

        return new_unit
    
    def __add__(self, other):
        '''Add two different units.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('other must be a unit')
        if other.dimension != self.dimension:
            raise ValueError('other must have the same dimension as the original') 
        converted_other = other.convert(self)
        if type(self) == unit:
            sum = unit(self.name, self.symbol, self.dimension, self.base_unit, 
                       self.base_units_per_unit, 
                       self.amount + converted_other.amount, self.prefix) 
        else:
            sum = type(self)(self.amount + converted_other.amount, self.prefix)
        return sum
    
    def __sub__(self, other):
        '''Subtract two different units.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('other must be a unit')
        if other.dimension != self.dimension:
            raise ValueError('other must have the same dimension as the original') 
        converted_other = other.convert(self)
        if type(self) == unit:
            diff = unit(self.name, self.symbol, self.dimension, self.base_unit, 
                        self.base_units_per_unit, 
                        self.amount - converted_other.amount, self.prefix) 
        else:
            diff = type(self)(self.amount - converted_other.amount, self.prefix)
        return diff
    
    def __mul__(self, other):
        '''Multiply a unit by a scalar or another unit.'''
        if isinstance(other, (int, float)):
            return unit(self.name, self.symbol, self.dimension, self.base_unit,
                         self.base_units_per_unit, self.amount * other,
                         self.prefix)
        elif isinstance(other, unit) or issubclass(type(other), unit):
            if self.dimension == other.dimension:
                new_name = f'{self.name} squared'
                new_symbol = f'{self.symbol}^2'
                new_dimension = f'{self.dimension} squared'
            else:
                new_name = f'{self.name}-{other.name}'
                new_symbol = f'{self.symbol}{other.symbol}'
                new_dimension = f'{self.dimension} * {other.dimension}'
            if new_dimension.lower() in derived_dimensions:
                new_dimension = derived_dimensions.get(new_dimension.lower())
            new_amount = self.amount * other.amount
            return unit(new_name, new_symbol, new_dimension, self.base_unit,
                        self.base_units_per_unit * other.base_units_per_unit,
                        new_amount
                        )
        
    def __rmul__(self, other):
        '''Multiply a unit by a scalar or another unit.'''
        return self.__mul__(other)
    
    def __truediv__(self, other):
        '''Divide a unit by a scalar or another unit.'''
        if isinstance(other, (int, float)):
            return unit(self.name, self.symbol, self.dimension, self.base_unit,
                         self.base_units_per_unit, self.amount / other,
                         self.prefix)
        elif isinstance(other, unit) or issubclass(type(other), unit):
            new_name = f'{self.name} per {other.name}'
            new_symbol = f'{self.symbol}/{other.symbol}'
            new_dimension = f'{self.dimension} / {other.dimension}'
            if new_dimension.lower() in derived_dimensions:
                new_dimension = derived_dimensions.get(new_dimension.lower())
            new_amount = self.amount / other.amount
            return unit(new_name, new_symbol, new_dimension, self.base_unit,
                        self.base_units_per_unit / other.base_units_per_unit,
                        new_amount
                        )

    def __str__(self):
        '''A string representation of the unit.'''
        prefix_symbol = prefix_symbols.get(self.prefix.lower(), '')
        return f'{self.amount} {prefix_symbol}{self.symbol}'

    def __repr__(self):
        return f'unit({self.name}, {self.symbol}, {self.dimension}, {self.base_unit}, {self.base_units_per_unit}, {self.amount}, {self.prefix})'
    
    def __eq__(self, other):
        '''Check to see if two units are equal.'''
        if self is other:
            return True
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            return False
        if self.dimension != other.dimension:
            return False
        
        converted_other = other.convert(self)
        return isclose(self.amount, converted_other.amount)
    
    def __ne__(self, other):
        '''Not equal to comparison.'''
        return not self.__eq__(other)
    
    def __lt__(self, other):
        '''Less than comparison.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('can only compare units to other units')
        if self.dimension != other.dimension:
            raise ValueError('units must have the same dimension to be compared')
        converted_other = other.convert(self)
        return self.amount < converted_other.amount
    
    def __le__(self, other):
        '''Less than or equal to comparison.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('can only compare units to other units')
        if self.dimension != other.dimension:
            raise ValueError('units must have the same dimension to be compared')
        converted_other = other.convert(self)
        return self.amount <= converted_other.amount
    
    def __gt__(self, other):
        '''Greater than comparison.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('can only compare units to other units')
        if self.dimension != other.dimension:
            raise ValueError('units must have the same dimension to be compared')
        converted_other = other.convert(self)
        return self.amount > converted_other.amount

    def __ge__(self, other):
        '''Greater than or equal to comparison.'''
        if not isinstance(other, unit) or not issubclass(type(other), unit):
            raise TypeError('can only compare units to other units')
        if self.dimension != other.dimension:
            raise ValueError('units must have the same dimension to be compared')
        converted_other = other.convert(self)
        return self.amount >= converted_other.amount
    

#___Length Units___
class meter(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('meter', 'm', 'length', None, 1, amount, prefix)

class plancklength(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('Planck length', 'lP', 'length', 'meter', 1.616255 * pow(10, -35), 
                         amount, prefix)

class angstrom(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('angstrom', 'Å', 'length', 'meter', pow(10, -10), 
                         amount, prefix)

class inch(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('inch', 'in', 'length', 'meter', 0.0254, amount, 
                         prefix)
        
    def toftinstr(self):
        '''Convert the amount into a string representing the feet and inches.'''
        feet = floor(self.convert(foot()).amount)
        remaining_inches = self.amount - (feet * 12)
        return f'{feet}\'{remaining_inches:.0f}\"'
    
    def toftinlist(self):
        '''Convert the amount into a list representing the feet and inches.'''
        feet = floor(self.convert(foot()).amount)
        remaining_inches = self.amount - (feet * 12)
        return [feet, remaining_inches]   

class foot(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('foot', 'ft', 'length', 'meter', 0.3048, amount, 
                         prefix)

class yard(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('yard', 'yd', 'length', 'meter', 0.9144, amount, 
                         prefix)

class mile(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('mile', 'mi', 'length', 'meter', 1609.344, amount, 
                         prefix)

class nauticalmile(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('nautical mile', 'nmi', 'length', 'meter', 1852, 
                         amount, prefix)

class astronomicalunit(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('astronomical unit', 'au', 'length', 'meter', 
                         149597870700, amount, prefix)

class lightyear(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('light year', 'ly', 'length', 'meter', 
                         9460730472580800, amount, prefix)
        
class parsec(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('parsec', 'pc', 'length', 'meter', 
                         30856775814913673, amount, prefix)
        
#___Temperature Units
class temperature(unit):
    def __init__(self, amount=0, prefix='', scale='Celsius'):
        if scale.lower() not in ('celsius', 'fahrenheit', 'kelvin'):
            raise ValueError('invalid temperature scale')
        super().__init__('degree', '°', 'temperature', None, 1.0, amount, prefix)
        self.scale = scale.capitalize()

    def convert(self, target_unit):
        if not isinstance(target_unit, temperature):
            raise TypeError('target unit must be a temperature')
        # Conversion logic depends on the scales:
        if self.scale == 'Celsius':
            if target_unit.scale == 'Fahrenheit':
                new_amount = (self.amount * 9/5) + 32
            elif target_unit.scale == 'Kelvin':
                new_amount = self.amount + 273.15
            else:  # Already in Celsius
                new_amount = self.amount
        elif self.scale == 'Fahrenheit':
            if target_unit.scale == 'Celsius':
                new_amount = (self.amount - 32) * 5/9
            elif target_unit.scale == 'Kelvin':
                new_amount = (self.amount - 32) * 5/9 + 273.15
            else:  # Already in Fahrenheit
                new_amount = self.amount
        elif self.scale == 'Kelvin':
            if target_unit.scale == 'Celsius':
                new_amount = self.amount - 273.15
            elif target_unit.scale == 'Fahrenheit':
                new_amount = (self.amount - 273.15) * 9/5 + 32
            else:  # Already in Kelvin
                new_amount = self.amount
        return temperature(new_amount, target_unit.prefix, target_unit.scale)

    def __str__(self):
        return f'{self.amount} {self.prefix}°{self.scale[0].upper()}'
    
class celsius(temperature):
    def __init__(self, amount=0, prefix=''):
        super().__init__(amount, prefix, 'Celsius')

class fahrenheit(temperature):
    def __init__(self, amount=0, prefix=''):
        super().__init__(amount, prefix, 'Fahrenheit')

class kelvin(temperature):
    def __init__(self, amount=0, prefix=''):
        super().__init__(amount, prefix, 'Kelvin')


#___Time Units___
class second(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('second', 's', 'time', None, 1, amount, prefix)    

class minute(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('minute', 'min', 'time', 'second', 60, amount, prefix)

class hour(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('hour', 'h', 'time', 'second', 3600, amount, prefix)

class day(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('day', 'd', 'time', 'second', 86400, amount, prefix)

class week(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('week', 'weeks', 'time', 'second', 604800, amount, prefix)

class common_year(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('year', 'yr', 'time', 'second', 31536000, amount, prefix)


#___Mass Units___
class gram(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('gram', 'g', 'mass', None, 1, amount, prefix)

class ounce(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('ounce', 'oz', 'mass', None, 28.349523125, amount, prefix)

class pound(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('pound', 'lb', 'mass', None, 453.59237, amount, prefix)

class tonne(unit):
    def __init__(self, amount = 0, prefix = ''):
        super().__init__('tonne', 't', 'mass', None, 1000000, amount, prefix)