'''Cosmic Core: Cosmic Random
\n\tAn upgrade of the built-in random module with new classes and functions.'''
from .cosmicdatastructures import *
from random import * #Imports all pre-existing functions.
from numpy import ndarray
import string
__all__ = ['seed', 'getstate', 'setstate', 'getrandbits', 'randrange', 
           'randint', 'choice', 'choices', 'shuffle', 'sample', 'random',
           'uniform', 'triangular', 'betavariate', 'expovariate',
           'gammavariate', 'gauss', 'lognormvariate', 'normalvariate',
           'vonmisesvariate', 'paretovariate', 'weibullvariate', 'Random',
           'SystemRandom', 'flipcoin', 'randstring', 'rolldice', 'parsedice',
           'dice']

#__New Functions__

def flipcoin():
    '''Simulate a coin flip and return Heads or Tails.'''
    return choice(['Heads', 'Tails'])

def randstring(length, characters = None):
    '''Generate a random string from a range of characters.'''
    if not isinstance(length, int):
        raise TypeError('length must be an int')
    if length <= 0:
      raise ValueError('length must be positive')
    
    if characters is None:
         characters = string.ascii_letters + string.digits
    if not isinstance(characters, str):
        raise TypeError('characters must be a string')
    
    return ''.join(choice(characters) for _ in range(length))

def rolldice(dice_objects):
    '''Roll one or more dice.'''
    if isinstance(dice_objects, str):
        dice_objects = parsedice(dice_objects)
    if isinstance(dice_objects, dice):
        return dice_objects.roll()
    elif isinstance(dice_objects, (list, linklist, dlinklist, ndarray)):
        if isinstance(dice_objects, (linklist, dlinklist)):
            dice_objects = dice_objects.pylist()
        if isinstance(dice_objects, ndarray):
            dice_objects = dice_objects.tolist()
        results = []
        for die in dice_objects:
            if not isinstance(die, dice):
                raise TypeError('all elements must be a dice object')
            results.append(die.roll())
        return results
    else:
        raise TypeError('dice_objects must be a die or list/NumPy array of dice')

def parsedice(dice_string):
    '''Parse a string like "2d6" and return a list of dice objects.
    \nThe string should follow the format [number of dice]d[number of sides].'''
    if not isinstance(dice_string, str):
      raise TypeError('dice_string must be a string')
    try:
        num_dice, num_sides = dice_string.lower().split('d')
        num_dice = int(num_dice)
        num_sides = int(num_sides)
    except ValueError:
        raise ValueError('invalid dice string format; should be [number of dice]d[number of sides]')
    if num_dice <= 0:
        raise ValueError('number of dice must be positive')
    if num_sides <= 0:
        raise ValueError('number of sides must be positive')
    
    dice_list = []
    for _ in range(num_dice):
        dice_list.append(dice(num_sides))
    return dice_list    


#__New Classes__

class dice(object):
    '''A representation of a die.'''

    def __init__(self, sides, face = None):
        if not isinstance(sides, int):
            raise TypeError('number of sides must be an int')
        if sides <= 0:
            raise ValueError('number of sides must be positive')
        if face is not None:
            if not isinstance(face, int):
                raise TypeError('face must be an int')
            if face < 0 or face > sides:
                raise ValueError('face must be between 1 and the number of sides')
        self.sides = sides
        self.face = face

    def __str__(self):
        'A string representation of the die.'
        if self.face is None:
            return f'{self.sides}-sided die'
        else:
            return f'{self.sides}-sided die showing {self.face}'
        
    def __repr__(self):
        if self.face is None:
            return f'dice({self.sides})'
        else:
            return f'dice({self.sides}, {self.face})'
    
    def roll(self):
        '''Roll the die.'''
        self.face = randint(1, self.sides)
        return self.face