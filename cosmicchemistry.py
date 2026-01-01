'''Cosmic Core: Cosmic Chemistry
\n\tA module containing useful tools for chemistry calculations.'''
from .cosmicdatabases import *
from .cosmicdatastructures import *
from .cosmicmath import *
from .cosmicstrings import capitalizefirstletter
from numpy import ndarray
import os
import re
__all__ = ['getchemicalname', 'getchemicalsymbol', 'gramstomoles', 
           'molestograms', 'molestoparticles', 'particlestomoles', 
           'gramstoparticles', 'particlestograms','getmolarmass', 'substance', 
           'reaction']
DB_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cosmicchemistry.db')


# ___Chemical Naming___
def getchemicalname(symbol):
    '''Give the name of an element or compound from its symbol.'''
    if not isinstance(symbol, str):
        raise TypeError('symbol must be a string')
    
    try:
        with sqlitedb(DB_LOCATION) as db:
            # 1. Check elements table
            query = 'SELECT name FROM elements WHERE symbol = ?'
            db.query(query, (symbol,))
            result = db.fetchone()
            if result:
                return result[0]  # Return the element name

            # 2. Check compounds table (common_name)
            query = 'SELECT common_name FROM compounds WHERE formula = ?'
            db.query(query, (symbol,))
            result = db.fetchone()
            if result and result[0]:  # Check if common_name exists and is not NULL
                return result[0]  # Return the common name

            # 3. Check compounds table (iupac_name)
            query = 'SELECT iupac_name FROM compounds WHERE formula = ?'
            db.query(query, (symbol,))
            result = db.fetchone()
            if result and result[0]:  # Check if iupac_name exists and is not NULL
                return result[0]  # Return the IUPAC name

        return None # Not in the database

    except Exception as e:
        print(f'Database lookup error: {e}')
        return None  # Handle database errors gracefully

def getchemicalsymbol(name):
    '''Give the symbol of an element or compound from its name.'''
    if not isinstance(name, str):
        raise TypeError('name must be a string')

    try:
        with sqlitedb(DB_LOCATION) as db:
            # 1. Check elements table
            query = 'SELECT symbol FROM elements WHERE name = ?'
            db.query(query, (name,))  # Name is already lowercase (see previous implementation)
            result = db.fetchone()
            if result:
                return result[0]

            # 2. Check compounds table (common_name)
            query = 'SELECT formula FROM compounds WHERE common_name = ? OR iupac_name = ?'
            db.query(query, (name, name))
            result = db.fetchone()
            if result:
                return result[0]

            return None  # Not found in the database

    except Exception as e:
        print(f'Database lookup error: {e}') # Log the error if you have a logger
        return None  # Handle database errors gracefully


# ___Mole Conversions___
def gramstomoles(substance, grams):
    '''Convert grams of a substance with a known chemical formula or molar mass
    to moles.'''
    if isinstance(substance, str) or isinstance(substance, list):
        return grams / getmolarmass(substance)
    elif isinstance(substance, int) or isinstance(substance, float):
        return grams / substance
    elif isinstance(substance, substance):
        return grams / substance.molar_mass

def molestograms(substance, moles):
    '''Convert moles of a substance with a known chemical formula or molar
    mass to grams.'''
    if not isinstance(moles, (int, float)):
        raise TypeError('moles must be an int or float')
    if isinstance(substance, str) or isinstance(substance, list):
        return moles * getmolarmass(substance)
    elif isinstance(substance, int) or isinstance(substance, float):
        return moles * substance
    elif isinstance(substance, substance):
        return moles * substance.molar_mass
    else:
        raise TypeError('substance must be a str, list, int, or float')

def molestoparticles(moles):
    '''Convert moles to a number of particles using Avogadro's Number.'''
    return moles * AVOGADROS_NUMBER

def particlestomoles(particles):
    '''Convert a number of particles to moles using Avogadro's Number.'''
    return particles / AVOGADROS_NUMBER

def gramstoparticles(substance, grams):
    '''Convert grams of a substance with a known chemical formula or molar mass
    to an amount of particles.'''
    return molestoparticles(gramstomoles(substance, grams))

def particlestograms(substance, particles):
    '''Convert an amount of particles of a substance with a known chemical
    formula or molar mass to grams.'''
    return molestograms(substance, particlestomoles(particles))


# ___Tools For Setting Up Chemical Compounds__
def _compoundtolist(compound):
    '''Convert a chemical formula into a list of elements and quantities.'''
    if not isinstance(compound, str):
        raise TypeError('compound must be a string')

    # Updated regex to handle parentheses and charges
    pattern = re.compile(r'([A-Z][a-z]*)(\d*)|(\()|(\))(\d*)')
    complist = []
    for match in pattern.finditer(compound):
        element, quantity, open_paren, close_paren, paren_quantity = match.groups()

        if element:
            complist.append(element)
            if quantity:
                complist.append(quantity)
            else:
                complist.append('1')
        elif open_paren:
            complist.append(open_paren)
        elif close_paren:
            complist.append(close_paren)
            if paren_quantity:
                complist.append(paren_quantity)
            else:
                complist.append('1')  #default it to '1' if none is present
    return complist

def getmolarmass(compound):
    '''Return the molar mass of a substance with a known chemical formula.'''

    if isinstance(compound, list):
        complist = compound
    elif isinstance(compound, str):
        complist = _compoundtolist(compound)
    else:
        raise TypeError('compound must be a string or a list')
    
    molar_mass = 0.0
    in_parentheses = False
    parentheses_start = 0
    parentheses_end = 0
    for i in range(0, len(complist)):
        add_to_mass = 0.0
        if not in_parentheses:
            if isinstance(complist[i], int) or isinstance(complist[i], float):
                pass
            elif isinstance(complist[i], str) and complist[i].isnumeric():
                pass
            elif complist[i].isalpha():
                element_symbol = complist[i]
                try:
                    with sqlitedb(DB_LOCATION) as db:
                        query = 'SELECT atomic_mass FROM elements WHERE symbol = ?'
                        db.query(query, (element_symbol,))
                        result = db.fetchone()
                        if result:
                            atomic_mass = result[0]
                            try:
                                if isinstance(complist[i + 1], int) or isinstance(complist[i + 1], float):
                                    add_to_mass = float(atomic_mass) * int(complist[i + 1])
                                elif isinstance(complist[i + 1], str) and complist[i + 1].isnumeric():
                                    add_to_mass = float(atomic_mass) * int(complist[i + 1])
                            except:
                                pass
                        else:
                            raise ValueError(f'element symbol not found in database: {element_symbol}')
                except Exception as e:
                    if isinstance(e, ValueError):
                        raise e
                    print(f'Database lookup error: {e}')
                    return None # Handle database errors gracefully
            elif complist[i] == '(':
                parentheses_start = i
                in_parentheses = True
        else:
            add_to_mass = 0.0
            if complist[i] == ')':
                parentheses_end = i
                in_parentheses = False
                add_to_mass = getmolarmass(complist[parentheses_start + 1:parentheses_end])
                try:
                    if isinstance(complist[i + 1], int) or isinstance(complist[i + 1], float):
                        add_to_mass *= int(complist[i + 1])
                    elif isinstance(complist[i + 1], str) and complist[i + 1].isnumeric():
                        add_to_mass *= int(complist[i + 1])
                except:
                    pass
        molar_mass += add_to_mass
    return molar_mass


#__Chemistry Classes__
class substance(object):
    '''Represents a chemical substance (element or compound).'''

    def __init__(self, identifier, id_type = 'formula'):
        self.substance_type = None
        self.id = None
        self.formula = None
        self.name = None
        self.molar_mass = None  # Computed later, but initialize it
        # Validate id_type
        if id_type not in ('formula', 'atomic_number', 'pubchem_cid'):
            raise ValueError('id_type must be \'formula\', \'atomic_number\', or \'pubchem_cid\'')

        try:  # Wrap all database interaction in a try block
            with sqlitedb(DB_LOCATION) as db:  # Use the sqlitedb context manager
                if id_type == 'atomic_number':
                    if not isinstance(identifier, int):
                        raise TypeError('identifier must be an integer for atomic_number')
                    if not 1 <= identifier <= 118:
                        raise ValueError('atomic number must be between 1 and 118')

                    query = 'SELECT symbol, name, atomic_mass FROM elements WHERE atomic_number = ?'
                    db.query(query, (identifier,))
                    result = db.fetchone()

                    if result:
                        self.substance_type = 'element'
                        self.id = identifier
                        self.formula = result[0]  # Element Symbol
                        self.name = result[1]
                        self.molar_mass = result[2]
                    else:
                        raise ValueError(f'element with atomic number {identifier} not found')

                elif id_type == 'pubchem_cid':
                    if not isinstance(identifier, int):
                        raise TypeError('identifier must be an integer for pubchem_cid')

                    query = 'SELECT formula, common_name, iupac_name FROM compounds WHERE pubchem_cid = ?'
                    db.query(query, (identifier,))
                    result = db.fetchone()

                    if result:
                        self.substance_type = 'compound'
                        self.id = identifier
                        self.formula = result[0]
                        if result[1]:
                            self.name = result[1] # Common name is not NULL
                        else:
                            self.name = result[2] #Use IUPAC name if common name is NULL
                        self.molar_mass = getmolarmass(self.formula)  # Calculate molar mass
                    else:
                        raise ValueError(f'compound with PubChem CID {identifier} not found.')

                elif id_type == 'formula':
                    if not isinstance(identifier, str):
                        raise TypeError('identifier must be a string for formula')

                    # Validate the formula
                    if not re.match(r'^[A-Za-z0-9()+\-\.\s]+$', identifier):
                        raise ValueError('invalid chemical formula format')

                    query = 'SELECT pubchem_cid, common_name, iupac_name FROM compounds WHERE formula = ?'
                    db.query(query, (identifier,))
                    result = db.fetchone()

                    if result:
                        self.substance_type = 'compound'
                        self.id = result[0] #PubChem CID
                        self.formula = identifier  # Store the formula
                        if result[1]:
                            self.name = result[1] #Common name is not NULL
                        else:
                            self.name = result[2] #Use IUPAC Name if common name is NULL
                        self.molar_mass = getmolarmass(self.formula)  # Calculate molar mass
                    else:  # Treat as an element lookup as a fallback, with atomic mass from elements table
                        query = 'SELECT atomic_number, name, atomic_mass FROM elements WHERE symbol = ?'
                        db.query(query, (identifier,))
                        result = db.fetchone()

                        if result:
                            self.substance_type = 'element'
                            self.id = result[0]
                            self.formula = identifier  # Element symbol
                            self.name = result[1]
                            self.molar_mass = result[2]
                        else:
                            # The substance is not in the database, it will be assumed to be a compound
                            self.substance_type = 'compound'
                            self.id = None
                            self.formula = identifier
                            self.name is None
                            self.molar_mass = getmolarmass(self.formula)

        except Exception as e:
            raise e
        #Basic checks in place, but they are barebones for the sake of the example
    
    def iselement(self):
        '''Return True if the substance is an element, False otherwise.'''
        try:
            with sqlitedb(DB_LOCATION) as db:
                query = 'SELECT COUNT(*) FROM elements WHERE symbol = ?'
                db.query(query, (self.formula,))
                result = db.fetchone()
                return result[0] > 0  # Returns True if a matching element exists
        except Exception as e:
            print(f'Database error in iselement: {e}')
            return False  # Handle database error (return False as a safe default)
    
    def getelements(self):
        '''Returns a list of the constituent elements in a chemical compound.'''
        try:
            with sqlitedb(DB_LOCATION) as db:
                query = '''
                    SELECT DISTINCT e.symbol
                    FROM compound_elements ce
                    JOIN elements e ON ce.atomic_number = e.atomic_number
                    JOIN compounds c ON ce.pubchem_cid = c.pubchem_cid
                    WHERE c.formula = ?
                '''
                db.query(query, (self.formula,))
                results = db.fetchall()
                elements = [row[0] for row in results]  # Extract element symbols from the results
                if elements:  # If elements were found in compound_elements, return them
                    return elements
                else: #If it wasn't found, then let's use parsing from _compoundtolist()
                    parsed_formula = _compoundtolist(self.formula)
                    elements = []
                    for element in parsed_formula:
                        if element.isalpha() and not element in elements:
                            elements.append(element)
                    return elements
        except Exception as e:
            print(f'Database error in getelements: {e}')
            #Parsing from _compoundtolist() now as a final fallback
            parsed_formula = _compoundtolist(self.formula)
            elements = []
            for element in parsed_formula:
                if element.isalpha() and not element in elements:
                    elements.append(element)
            return elements

    def ishydrocarbon(self):
        '''Return True if the substance is a hydrocarbon, False otherwise.'''
        if self.iselement():
            return False
        else:
            return all(e in ['H', 'C'] for e in self.getelements())
    
    def __str__(self):
        '''Return a string representation of the substance.'''
        if self.name is not None:
            return f'{capitalizefirstletter(self.name)} ({self.formula}) (Molar Mass: {self.molar_mass:.3f} g/mol)'
        if getchemicalname(self.formula) is not None:
            name = getchemicalname(self.formula)
            return f'{capitalizefirstletter(name)} ({self.formula}) (Molar Mass: {self.molar_mass:.3f} g/mol)'
        elif self.ishydrocarbon():
            return f'Hydrocarbon ({self.formula}) (Molar Mass: {self.molar_mass:.3f} g/mol)'
        else:
            return f'Chemical Compound ({self.formula}) (Molar Mass: {self.molar_mass:.3f} g/mol)'

    def __repr__(self):
        return f'substance(\'{self.formula}\')'
    
    def __eq__(self, other):
        '''Return True if self equals other, False otherwise.'''
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.formula == other.formula
    
class reaction(object):
    '''Represents a chemical reaction, with reactants and products.'''

    def __init__(self, reactants, products):
        if not isinstance(reactants, (list, linklist, dlinklist, ndarray)):
            raise TypeError('reactants must be a list, linked list, or NumPy array')
        if not isinstance(products, (list, linklist, dlinklist, ndarray)):
            raise TypeError('products must be a list, linked list, or NumPy array')
        if isinstance(reactants, ndarray):
            reactants = reactants.tolist()
        if isinstance(products, ndarray):
            products = products.tolist()
        if not all(isinstance(item, substance) for item in reactants):
            raise TypeError('all elements in reactants must be substances')
        if not all(isinstance(item, substance) for item in products):
            raise TypeError('all elements in products must be substances')
        self.reactants = reactants
        self.products = products

    def __str__(self):
        '''Return a string representation of the reaction.'''
        reactant_strings = [str(reactant.formula) for reactant in self.reactants]
        product_strings = [str(product.formula) for product in self.products]
        return ' + '.join(reactant_strings) + ' → ' + ' + '.join(product_strings)

    def __repr__(self):
        return f'reaction({repr(self.reactants)}, {repr(self.products)})'