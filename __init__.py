'''
Cosmic Core v0.7.0: A foundational library of reusable components for Python developers.

Cosmic Core is composed of the following modules:

* **Cosmic Algebra** (`cosmicalgebra.py`): Data types and functions for various algebraic fields.
* **Cosmic Algorithms** (`cosmicalgorithms.py`): Sorting and searching algorithms.
* **Cosmic Chemistry** (`cosmicchemistry.py`): Tools for chemical calculations, mole conversions, and compound analysis.
* **Cosmic Console** (`cosmicconsole.py`): Tools to enhance console output.
* **Cosmic Cryptography** (`cosmiccryptography.py`): Tools for encryption, decryption, hashing, and key generation.
* **Cosmic Databases** (`cosmicdatabases.py`): Tools for working with SQLite databases.
* **Cosmic Data Structures** (`cosmicdatastructures.py`): Basic data structures.
* **Cosmic File I/O** (`cosmicfileio.py`): Functions for reading and writing files in various formats (text, binary, CSV, JSON).
* **Cosmic Geometry** (`cosmicgeometry.py`): Data types and functions for representing and manipulating geometric shapes.
* **Cosmic Infinity** (`cosmicinfinity.py`): Data types and functions for infinite numbers and sets (Aleph, Beth, ordinals).
* **Cosmic Math** (`cosmicmath.py`):  Advanced mathematical functions and classes.
* **Cosmic Numerals** (`cosmicnumerals.py): Tools for converting numerals.
* **Cosmic Random** (`cosmicrandom.py`): Tools for dealing with random generation.
* **Cosmic Strings** (`cosmicstrings.py`): Tools for string manipulations, casing, and analysis.
* **Cosmic System** (`cosmicsystem.py`): Tools for system and file management.
* **Cosmic Units** (`cosmicunits.py`):  Simplifies working with units, providing conversions and unit arithmetic.
* **Cosmic Visuals** (`cosmicvisuals.py`):  Functions for drawing objects defined in the Geometry Module using Turtle.

'''
__version__ = '0.7.0'

#___Library Information___
def getccversion():
    '''Return the current version of Cosmic Core.'''
    return __version__
import subprocess

#Install required dependencies automatically
def install(library):
    '''Install a Python library, assuming it is not already installed.'''
    if not isinstance(library, str):
        raise TypeError('library name must be a string')
    try:
        __import__(library)
    except ImportError:
        subprocess.check_call(['python', '-m', 'pip', 'install', library])

install('cryptography')
install('numpy')

#Make all modules accessible with the command `from cosmiccore import`
from .cosmicalgebra import *
from .cosmicalgorithms import *
from .cosmicchemistry import *
from .cosmicconsole import *
from .cosmiccryptography import *
from .cosmicdatabases import *
from .cosmicfileio import *
from .cosmicdatastructures import *
from .cosmicgeometry import *
from .cosmicinfinity import *
from .cosmicmath import *
from .cosmicnumerals import *
from .cosmicrandom import *
from .cosmicstrings import *
from .cosmicsystem import *
from .cosmicunits import *
from .cosmicvisuals import *