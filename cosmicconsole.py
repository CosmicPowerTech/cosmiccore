'''Cosmic Core: Cosmic Console
\n\tA library of functions designed to enhance console output.'''
import os
import ctypes
__all__ = ['printcclogo', 'printunorderedlist', 'printorderedlist', 'ansibold',
           'ansiitalic', 'ansiunderline', 'ansiblink', 'ansicolor',
           'ansibgcolor', 'clearconsole']

#__Cosmic Core Logo__
cosmic_core_logo = '''
              CCC              
          CCCC   CCCC          
      CCCC           CCCC      
   CCC       CCCCC       CCC   
CCC        CCCCCCCCC        CCC
C  CCCCC     CCCCC     CCCCC  C
C  CC   CCCC       CCCC   CC  C
C  C CCCC   CCC CCC   CCCC    C
C  C     CCCC  C  CCCC        C
C  C           C  C           C
C  CC          C  C       CC  C
CCC  CCCCC     C  C   CCCC  CCC
   CCC    CCC  C  CCCC   CCC   
      CCCC     C     CCCC      
          CCCC C CCCC          
              CCC              
'''

def printcclogo(color = None):
    '''Display the Cosmic Core logo in ASCII art to the console.'''
    if color is None:
        print(cosmic_core_logo)
    else:
        print(ansicolor(cosmic_core_logo, color))


#__Lists__
def printunorderedlist(data, bullet = '•', indent = 0):
    '''Display an iterable to the console in the form of an unordered (bullet)
    list.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    
    if not isinstance(bullet, str):
        raise TypeError('bullet must be a string')

    if not isinstance(indent, int) or indent < 0:
        raise ValueError('indent must be a non-negative integer')
    
    indent_str = ' ' * indent

    for item in data:
        if hasattr(item, '__iter__') and not isinstance(item, str):
            # If the item is an iterable (but not a string), call printunorderedlist recursively
            print(f'{indent_str}{bullet}')
            printunorderedlist(item, bullet, indent + 2)
        else:
            print(f'{indent_str}{bullet} {str(item)}')

def printorderedlist(data, start_num = 1, indent = 0):
    '''Display an iterable to the console as an ordered list.'''
    if not hasattr(data, '__iter__'):
        raise TypeError('data must be an iterable')
    
    if not isinstance(start_num, int) or start_num <= 0:
        raise ValueError('start_num must be a positive integer')
    
    if not isinstance(indent, int) or indent < 0:
        raise ValueError('indent must be a non-negative integer')
    
    indent_str = ' ' * indent
    
    num = start_num
    for item in data:
        print(f'{indent_str}{num}. {str(item)}')
        num += 1


#__ANSI Formatting (Not supported on all systems)__
def _hasansisupport():
    '''Check if the system supports ANSI escape codes.'''
    if os.name != 'nt':
        # Non-Windows systems generally support ANSI escape codes
        return True
    else:
        # Windows 10 and later support ANSI escape codes in the console
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except:
            return False

def ansibold(text):
    '''Make a string boldfaced using ANSI escape codes (Support varies).'''
    return f'\x1b[1m{text}\x1b[22m' if _hasansisupport() else text

def ansiitalic(text):
    '''Make a string italic using ANSI escape codes (Support varies).'''
    return f'\x1b[3m{text}\x1b[23m' if _hasansisupport() else text

def ansiunderline(text):
    '''Underline a string using ANSI escape codes (Support varies).'''
    return f'\x1b[4m{text}\x1b[24m' if _hasansisupport() else text

def ansiblink(text):
    '''Make a string blink using ANSI escape codes (Support varies).'''
    return f'\x1b[5m{text}\x1b[25m' if _hasansisupport() else text

def ansicolor(text, color = 'white'):
    '''Give a string color using ANSI escape codes (Support varies).'''
    TEXT_COLORS = {'black':'30', 'red':'31', 'green':'32', 'yellow':'33',
                   'blue':'34', 'magenta':'35', 'cyan':'36', 'white':'37',
                   'bright black':'90', 'bright red':'91', 'bright green':'92',
                   'bright yellow':'93', 'bright blue':'94', 
                   'bright magenta':'95', 'bright cyan':'96', 
                   'bright white':'97'}
    
    if not isinstance(color, str):
        raise TypeError('color must be a str')
    
    if color.lower() not in TEXT_COLORS:
        raise ValueError('invalid color')
    
    return f'\x1b[{TEXT_COLORS.get(color)}m{text}\x1b[39m' if _hasansisupport() else text

def ansibgcolor(text, color = 'black'):
    '''Give a string a background color using ANSI escape codes (Support varies).'''
    BG_COLORS = {'black':'40', 'red':'41', 'green':'42', 'yellow':'43',
                'blue':'44', 'magenta':'45', 'cyan':'46', 'white':'47',
                'bright black':'100', 'bright red':'101', 'bright green':'102',
                'bright yellow':'103', 'bright blue':'104',
                'bright magenta':'105','bright cyan':'106',
                'bright white':'107'}
    
    if not isinstance(color, str):
        raise TypeError('color must be a str')
    
    if color.lower() not in BG_COLORS:
        raise ValueError('invalid color')
    
    return f'\x1b[{BG_COLORS.get(color)}m{text}\x1b[49m' if _hasansisupport() else text


#__Cleanup__
def clearconsole():
    'Clear the console.'
    os.system('cls' if os.name == 'nt' else 'clear')