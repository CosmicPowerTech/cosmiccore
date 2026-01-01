'''Cosmic Core: Cosmic Numerals
\n\t A library of conversion functions for various numeral systems.'''
from .cosmicstrings import transcribe
__all__ = ['toromannumeral', 'fromromannumeral', 'togreeknumeral', 
           'fromgreeknumeral', 'toarabicnumeral', 'fromarabicnumeral',
           'tojapanesenumeral','fromjapanesenumeral']

#___Numeral Conversions___
def toromannumeral(num):
    '''Convert an integer to its Roman numeral representation.'''
    if not isinstance(num, int):
        raise TypeError('input must be an integer')
    if num < 1:
        raise ValueError('input must be a positive integer')
    
    roman_map = { 1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 
                 90: 'XC', 100: 'C', 400: 'XD', 500: 'D', 900: 'CM', 1000: 'M'}
    i = 12
    result = ''
    while num != 0:
        if list(roman_map.keys())[i] <= num:
            result += list(roman_map.values())[i]
            num -= list(roman_map.keys())[i]
        else:
            i -= 1
    return result

def fromromannumeral(roman):
    '''Convert a Roman numeral to its integer representation.'''
    if not isinstance(roman, str):
        raise TypeError('input must be a string')

    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0

    for char in reversed(roman):
        if char not in roman_map:
            raise ValueError('invalid Roman numeral character')
        current_value = roman_map[char]
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value

    return total

def togreeknumeral(num):
    '''Convert an integer to its Greek numeral representation.'''
    if not isinstance(num, int):
        raise TypeError('input must be an integer')
    if num < 1:
        raise ValueError('input must be a positive integer')
    greek_map = {1: 'Α', 2: 'Β', 3: 'Γ', 4: 'Δ', 5: 'Ε', 6: 'Ϛ', 7: 'Ζ',
                 8: 'Η', 9: 'Θ', 10: 'Ι', 20: 'Κ', 30: 'Λ', 40: 'Μ', 50: 'Ν',
                 60: 'Ξ', 70: 'Ο', 80: 'Π', 90: 'Ϙ', 100: 'Ρ', 200: 'Σ',
                 300: 'Τ', 400: 'Υ', 500: 'Φ', 600: 'Χ', 700: 'Ψ', 800: 'Ω',
                 900: 'Ϡ', 1000: ',Α', 2000: ',Β', 3000: ',Γ', 4000: ',Δ',
                 5000: ',Ε', 6000: ',Ϛ', 7000: ',Ζ', 8000: ',Η', 9000: ',Θ'}
    result = ''
    for i in range(len(greek_map) - 1, -1, -1):
        while num >= list(greek_map.keys())[i]:
            result += list(greek_map.values())[i]
            num -= list(greek_map.keys())[i]
    return result

def fromgreeknumeral(greek):
    '''Convert a Greek numeral to its integer representation.'''
    if not isinstance(greek, str):
        raise TypeError('input must be a string')

    greek_map = {
        'Α': 1, 'Β': 2, 'Γ': 3, 'Δ': 4, 'Ε': 5, 'Ϛ': 6, 'Ζ': 7, 'Η': 8, 'Θ': 9,
        'Ι': 10, 'Κ': 20, 'Λ': 30, 'Μ': 40, 'Ν': 50, 'Ξ': 60, 'Ο': 70, 'Π': 80,
        'Ϙ': 90, 'Ρ': 100, 'Σ': 200, 'Τ': 300, 'Υ': 400, 'Φ': 500, 'Χ': 600,
        'Ψ': 700, 'Ω': 800, 'Ϡ': 900, ',Α': 1000, ',Β': 2000, ',Γ': 3000,
        ',Δ': 4000, ',Ε': 5000, ',Ϛ': 6000, ',Ζ': 7000, ',Η': 8000, ',Θ': 9000
    }

    total = 0
    for char in greek:
        if char not in greek_map:
            raise ValueError(f"Invalid Greek numeral character: {char}")
        total += greek_map[char]

    return total

def toarabicnumeral(num, variant = 'arabic'):
    '''Convert an integer or float to its Eastern Arabic numeral 
    representation.'''
    if not isinstance(num, (int, float)):
        raise TypeError('input must be an integer or float')
    arabic_map = {0: '٠', 1: '١', 2: '٢', 3: '٣', 4: '٤', 5: '٥', 6: '٦',
                  7: '٧', 8: '٨', 9: '٩'}
    persian_map = {0: '۰', 1: '۱', 2: '۲', 3: '۳', 4: '۴', 5: '۵', 6: '۶',
                   7: '۷', 8: '۸', 9: '۹'}
    if variant.lower() == 'arabic':
        return transcribe(str(num).replace('.', '٫'), arabic_map)
    elif variant.lower() == 'persian':
        return transcribe(str(num).replace('.', '٫'), persian_map)
    else:
        raise ValueError('invalid variant')
    
def fromarabicnumeral(arabic, variant='arabic'):
    '''Convert an Eastern Arabic numeral to its integer or float representation.'''
    if not isinstance(arabic, str):
        raise TypeError('input must be a string')

    arabic_map = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6',
                  '٧': '7', '٨': '8', '٩': '9', '٫': '.'}
    persian_map = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6',
                   '۷': '7', '۸': '8', '۹': '9', '٫': '.'}

    if variant.lower() == 'arabic':
        numeral_map = arabic_map
    elif variant.lower() == 'persian':
        numeral_map = persian_map
    else:
        raise ValueError('invalid variant')

    try:
        # Replace Eastern Arabic or Persian numerals with Western numerals
        western_numeral = ''.join(numeral_map[char] if char in numeral_map else char for char in arabic)
        # Convert to integer or float
        return int(western_numeral) if '.' not in western_numeral else float(western_numeral)
    except KeyError:
        raise ValueError('input contains invalid characters')
    except ValueError:
        raise ValueError('input is not a valid numeral')
    
def tojapanesenumeral(num):
    '''Convert an integer or float to its Japanese numeral representation.'''
    if not isinstance(num, (int, float)):
        raise TypeError('input must be an integer or float')
    if num < 0:
        return "負" + tojapanesenumeral(-num)
    if num == 0:
        return "零"

    japanese_numerals = {
        1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九",
        10: "十", 100: "百", 1000: "千", 10000: "万", 100000000: "億", 
        1000000000000: "兆", 10000000000000000: "京", 100000000000000000000: "垓",
        1000000000000000000000000: "𥝱", 10000000000000000000000000000: "穣",
        100000000000000000000000000000000: "溝",
        1000000000000000000000000000000000000: "澗",
        10000000000000000000000000000000000000000: "正",
        100000000000000000000000000000000000000000000: "載",
        1000000000000000000000000000000000000000000000000: "極",
        10000000000000000000000000000000000000000000000000000: "恒河沙",
        100000000000000000000000000000000000000000000000000000000: "阿僧祇",
        1000000000000000000000000000000000000000000000000000000000000: "那由他",
        10000000000000000000000000000000000000000000000000000000000000000: "不可思議",
        100000000000000000000000000000000000000000000000000000000000000000000: "無量大数",
    }

    decimal_numerals = {
        pow(10, -1): "分", pow(10, -2): "厘", pow(10, -3): "毛", pow(10, -4): "糸",
        pow(10, -5): "忽", pow(10, -6): "微", pow(10, -7): "繊", pow(10, -8): "沙",
        pow(10, -9): "塵", pow(10, -10): "埃"
    }

    result = ''
    integer_part, decimal_part = str(num).split('.') if '.' in str(num) else (str(num), '0')

    #Handle the integer part
    for power_of_ten in sorted(japanese_numerals.keys(), reverse=True):
        if int(integer_part) >= power_of_ten:
            quotient = int(integer_part) // power_of_ten
            if quotient > 1:
                result += tojapanesenumeral(quotient)
            result += japanese_numerals[power_of_ten]
            integer_part = str(int(integer_part) % power_of_ten)

    #Handle the decimal part
    if decimal_part != '0':
        decimal_digits = [int(d) for d in decimal_part]
        for i, digit in enumerate(decimal_digits):
            if digit > 0:
                result += tojapanesenumeral(digit)  #Convert digit to Japanese numeral
                result += decimal_numerals[pow(10, - (i + 1))]  #Add the corresponding numeral
    return result

def fromjapanesenumeral(japanese):
    '''Convert a Japanese numeral to its integer or float representation.'''
    if not isinstance(japanese, str):
        raise TypeError('input must be a string')

    japanese_numerals = {
        "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
        "十": 10, "百": 100, "千": 1000, "万": 10000, "億": 100000000, 
        "兆": 1000000000000, "京": 10000000000000000, "垓": 100000000000000000000,
        "𥝱": 1000000000000000000000000, "穣": 10000000000000000000000000000,
        "溝": 100000000000000000000000000000000, "澗": 1000000000000000000000000000000000000,
        "正": 10000000000000000000000000000000000000000,
        "載": 100000000000000000000000000000000000000000000,
        "極": 1000000000000000000000000000000000000000000000000,
        "恒河沙": 10000000000000000000000000000000000000000000000000000,
        "阿僧祇": 100000000000000000000000000000000000000000000000000000000,
        "那由他": 1000000000000000000000000000000000000000000000000000000000000,
        "不可思議": 10000000000000000000000000000000000000000000000000000000000000000,
        "無量大数": 100000000000000000000000000000000000000000000000000000000000000000000,
    }

    decimal_numerals = {
        "分": pow(10, -1), "厘": pow(10, -2), "毛": pow(10, -3), "糸": pow(10, -4),
        "忽": pow(10, -5), "微": pow(10, -6), "繊": pow(10, -7), "沙": pow(10, -8),
        "塵": pow(10, -9), "埃": pow(10, -10)
    }

    total = 0
    current_value = 0
    decimal_value = 0
    is_decimal = False

    for char in japanese:
        if char in japanese_numerals:
            current_value = current_value * japanese_numerals[char] if current_value else japanese_numerals[char]
        elif char in decimal_numerals:
            is_decimal = True
            decimal_value += current_value * decimal_numerals[char]
            current_value = 0
        elif char == "負":
            total *= -1
        else:
            raise ValueError(f"Invalid Japanese numeral character: {char}")

        if not is_decimal and char in japanese_numerals and japanese_numerals[char] >= 10:
            total += current_value
            current_value = 0

    total += current_value
    return total + decimal_value if is_decimal else total