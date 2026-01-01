'''Cosmic Core: Cosmic System
\n\tA library of functions designed for system management.'''
import os
import platform
import shutil
import stat
import sys
__all__ = ['getos', 'gethostname', 'getusername', 'getpyverstr',
           'createdirectory', 'deletedirectory', 'filecount', 'createfile',
           'touchfile', 'deletefile', 'movefile', 'copyfile', 'getfilesize']


#___System Information___
def getos():
    '''Return the operating system the code is running on.'''
    if sys.platform.startswith('aix'):
        return 'AIX'
    elif sys.platform.startswith('cygwin'):
        return 'Cygwin'
    elif sys.platform.startswith('darwin'):
        return 'macOS'
    elif sys.platform.startswith('emscripten'):
        return 'Emscripten'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform.startswith('wasi'):
        return 'WASI'
    elif sys.platform.startswith('win'):
        return 'Windows'
    else:
        return 'Unknown OS'
    
def gethostname():
    '''Return the hostname of the system.'''
    return platform.node()

def getusername():
    '''Return the current username.'''
    return os.getlogin()

def getpyverstr():
    '''Return the version of Python that is being used as a string.'''
    ver = sys.version_info
    ver_number = f'{ver.major}.{ver.minor}.{ver.micro}'
    if ver.releaselevel == 'final':
        return ver_number
    else:
        return f'{ver_number} {ver.releaselevel.capitalize()} {ver.serial}'


#___File Management___
def createdirectory(directory_path):
    '''Create a directory at the specified path.'''
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok = True)
    except OSError as e:
        raise e

def deletedirectory(directory_path, force = False,  ignore_errors=False):
    '''Delete the directory at the specified path.'''
    if not os.path.exists(directory_path):
        raise OSError(f'{directory_path} not found')
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f'{directory_path} is not a directory')

    try:
        if force:
            shutil.rmtree(directory_path, ignore_errors=ignore_errors) 
        else:
            if os.listdir(directory_path):
                raise ValueError(f'directory is not empty: {directory_path}, use force=True to delete recursively')
            os.rmdir(directory_path)
    except OSError as e:
        raise e
    except ValueError as e:
        raise e

def filecount(directory_path):
    '''Return the amount of files in a certain directory.'''
    return len(os.listdir(directory_path))
    
def createfile(filename, contents = ''):
    '''Create a new file with optional content.'''
    try:
        with open(filename, 'w') as f:
            f.write(contents)
    except OSError as e:
        raise e

def touchfile(filename):
    '''Create an empty file if it doesn't exist, or update its timestamp if it does.
    \nEmulates the UNIX touch command.'''
    try:
        os.utime(filename, None) #This directly updates the timestamp if the file exists
    except FileNotFoundError: 
        #File doesn't exist, so create it
        with open(filename, 'w') as f:
            pass
    except OSError as e:
        raise e
    
def deletefile(filename, force = False):
    '''Delete a file.'''
    if not os.path.exists(filename):
        raise FileNotFoundError(f'{filename} not found')
    if not os.path.isfile(filename):
        raise OSError(f'{filename} is not a file')
    
    try:
        if force and platform.system() == "Windows":
            os.chmod(filename, stat.S_IWRITE)
        os.remove(filename)
    except OSError as e:
        raise e

def movefile(filename, source, destination):
    '''Move a file from one directory to another.'''
    if not os.path.exists(os.path.join(source, filename)):
        raise FileNotFoundError(f'{filename} not found')
    if not os.path.isfile(os.path.join(source, filename)):
        raise OSError(f'{filename} is not a file')
    
    try:
        source_path = os.path.join(source, filename)
        destination_path = os.path.join(destination, filename)
        shutil.move(source_path, destination_path)
    except FileNotFoundError as e:
        raise e
    except OSError as e:
        raise e

def copyfile(filename, source, destination, preserve_metadata = True,
            overwrite = False):
    '''Copy a file from one directory to another.'''
    if not os.path.exists(os.path.join(source, filename)):
        raise FileNotFoundError(f'{filename} not found')
    if not os.path.isfile(os.path.join(source, filename)):
        raise OSError(f'{filename} is not a file')
    if os.path.isfile(os.path.join(destination, filename)) and not overwrite:
        raise FileExistsError(f'destination already exists, use overwrite=True to allow overwriting')
    
    try:
        source_path = os.path.join(source, filename)
        destination_path = os.path.join(destination, filename)
        if preserve_metadata:
            shutil.copy2(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
    except FileNotFoundError as e:
        raise e
    except OSError as e:
        raise e

def getfilesize(filename):
    '''Return the size of a file in bytes.'''
    if not os.path.exists(filename):
        raise FileNotFoundError(f'{filename} not found')
    if not os.path.isfile(filename):
        raise OSError(f'{filename} is not a file')
    
    try:
        return os.path.getsize(filename)
    except FileNotFoundError as e:
        raise e
    except OSError as e:
        raise e