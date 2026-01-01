'''Cosmic Core: Cosmic Strings
\n\t A library of functions for string manipulation, casing, and analysis.'''
import string
__all__ = ['reverse', 'ispalindrome', 'transcribe', 'removepunctuation',
           'tokenize', 'capitalizefirstletter', 'lowercamelcase',
           'uppercamelcase', 'snakecase', 'kebabcase', 'wordcount',
           'levenshteindistance']

#___String Manipulation___
def reverse(input):
    '''Take a string and reverses its contents.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    return input[::-1]

def ispalindrome(input):
    '''Return True if input is the same as when it's reversed.
    \nThis function is case insensitive.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    if input.lower() == reverse(input.lower()):
        return True
    else:
        return False

def transcribe(input, replacements):
    '''Replace characters in a string based on a dictionary of replacements.
    \nPreconditions: input is a string, and replacements is a dictionary.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    if not isinstance(replacements, dict):
        raise TypeError('replacements must be a dict')
    output = input
    for i in replacements:
        output=output.replace(str(i), replacements[i])
    return output

def removepunctuation(input):
    '''Remove all punctuation from a string.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    return input.translate(str.maketrans('', '', string.punctuation))

def tokenize(input, lowercase = True, remove_punctuation = True,
             split_on_whitespace = True):
    '''Tokenize a string of text into a list of tokens.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    processed_input = input

    if lowercase:
        processed_input = processed_input.lower()

    if remove_punctuation:
        processed_input = removepunctuation(processed_input)
    
    if split_on_whitespace:
        tokens = processed_input.split()
    else:
        tokens = list(processed_input)

    return tokens


#___ Case Conversions___
def capitalizefirstletter(input):
    '''Capitalize the first letter in the string.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    inputlist = list(input)

    for index, char in enumerate(inputlist):
        if char.islower():
            inputlist[index] = char.upper()
            break

    output = ''.join(inputlist)
    return output

def lowercamelcase(input):
    '''Convert a string to lower camel case.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    words = removepunctuation(input).split()
    if len(words) > 0:
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    else:
      return ''
    
def uppercamelcase(input):
    '''Convert a string to upper camel case.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    words = removepunctuation(input).split()
    if len(words) > 0:
        return ''.join(word.capitalize() for word in words)
    else:
      return ''
    
def snakecase(input):
    '''Convert a string to snake case.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    words = removepunctuation(input).split()
    if len(words) > 0:
        return ''.join(word.lower() + '_' for word in words)[:-1]
    else:
      return ''
    
def kebabcase(input):
    '''Convert a string to kebab case.'''
    if not isinstance(input, str):
        raise TypeError('input must be a string')
    words = removepunctuation(input).split()
    if len(words) > 0:
        return ''.join(word.lower() + '-' for word in words)[:-1]
    else:
      return ''
    

#___String Analysis___
def wordcount(text):
    '''Return the number of words in a string.'''
    words = text.split()
    return len(words)

def levenshteindistance(str1, str2):
    '''Compute the Levenshtein distance between two strings.'''
    if len(str1) < len(str2):
        return levenshteindistance(str2, str1)

    if len(str2) == 0:
        return len(str1)

    previous_row = range(len(str2) + 1)
    for i, char1 in enumerate(str1):
        current_row = [i + 1]
        for j, char2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (char1 != char2)

        current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]