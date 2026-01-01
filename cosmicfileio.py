'''Cosmic Core: Cosmic File I/O
\n\tA library of functions for reading and writing files in various formats.'''
import csv
import json
import gzip
import os
import tarfile
import zipfile
__all__ = ['readtextfile', 'writetextfile', 'readbinaryfile', 'writebinaryfile',
           'readcsvfile', 'writecsvfile', 'readjsonfile', 'writejsonfile',
           'compresszipfile', 'extractzipfile', 'compressgzipfile',
           'extractgzipfile']


#___Reading and Writing Text Files___
def readtextfile(file_path):
    '''Read the contents of a text file.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def writetextfile(file_path, content):
    '''Write content to a text file.'''
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


#___Reading and Writing Binary Files___
def readbinaryfile(file_path):
    '''Read the contents of a binary file.'''
    with open(file_path, 'rb') as file:
        return file.read()

def writebinaryfile(file_path, content):
    '''Write the contents of a binary file.'''
    with open(file_path, 'wb') as file:
        file.write(content)


#___Reading and Writing CSV Files___
def readcsvfile(file_path):
    '''Read and parse a CSV file.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def writecsvfile(file_path, data):
    '''Write data to a CSV file.'''
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


#___Reading and Writing JSON Files___
def readjsonfile(file_path):
    '''Read and parse a JSON file.'''
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def writejsonfile(file_path, data):
    '''Write data to a JSON file.'''
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

#___Compressing and Decompressing Files___
def compresszipfile(file_paths, zip_file_path):
    '''Compress files or directories into a zip archive.'''
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if os.path.isdir(file_path):
                for root, _, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, os.path.dirname(file_path))
                        zipf.write(full_path, arcname)
            else:
                zipf.write(file_path, os.path.basename(file_path))


def extractzipfile(zip_file_path, dest_dir):
    '''Extract the contents of a zip archive to a destination directory.'''
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extractall(dest_dir)


def compressgzipfile(file_path, gzip_file_path):
    '''Compress a file into a gzip archive.'''
    with open(file_path, 'rb') as f_in:
        with gzip.open(gzip_file_path, 'wb') as f_out:
            f_out.writelines(f_in)


def extractgzipfile(gzip_file_path, dest_dir):
    '''Extract the contents of a gzip archive to a destination directory.'''
    file_name = os.path.basename(gzip_file_path).replace('.gz', '')
    dest_file_path = os.path.join(dest_dir, file_name)
    with gzip.open(gzip_file_path, 'rb') as f_in:
        with open(dest_file_path, 'wb') as f_out:
            f_out.write(f_in.read())

def createtararchive(source, destination, compression=None):
    '''Create a tar archive of a file or directory.
    \nPrecondition: source is the path to the file or directory to archive,'''
    mode = 'w'
    if compression == 'gz':
        mode = 'w:gz'
    elif compression == 'bz2':
        mode = 'w:bz2'
    elif compression == 'xz':
        mode = 'w:xz'
    
    with tarfile.open(destination, mode) as tar:
        tar.add(source, arcname=os.path.basename(source))


def extracttararchive(archive, destination):
    '''Extract a tar archive to a destination directory.'''
    if not os.path.exists(destination):
        os.makedirs(destination)
    with tarfile.open(archive, 'r:*') as tar:  #Autodetect compression
        tar.extractall(destination)