'''Cosmic Core: Cosmic Cryptography
\n\tA library of encryption, decryption, and hashing functions.'''
import cryptography

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.decrepit.ciphers.algorithms import Blowfish
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15, OAEP
from cryptography.hazmat.primitives.asymmetric import utils

import hashlib

from os import urandom
__all__ = ['caesarencrypt', 'caesardecrypt', 'aesencrypt', 'aesdecrypt',
           'blowfishencrypt', 'blowfishdecrypt', 'rsagenkey', 'rsaencrypt',
           'rsadecrypt', 'sha256', 'sha512', 'md5']

#___Caesar Cipher___
def caesarencrypt(text, shift):
    '''Encrypt text using a Caesar cipher with the given shift.'''
    result = ''
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
        else:
            shifted_char = char
        result += shifted_char
    return result

def caesardecrypt(text, shift):
    '''Decrypt text encrypted with a Caesar cipher.'''
    return caesarencrypt(text, -shift)


#___Symmetric Encryption___
def aesencrypt(key, plaintext, associated_data=None):
    '''Encrypt plaintext using AES in CBC mode.'''
    backend = default_backend()
    if associated_data is None:
        associated_data = b''

    #Pad the plaintext to a multiple of 16 bytes
    padding_length = 16 - (len(plaintext.encode('utf-8')) % 16)
    plaintext = plaintext + (chr(padding_length) * padding_length)

    cipher = Cipher(algorithms.AES(key), modes.CBC(bytes(16)), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    if associated_data:
        ciphertext = encryptor.update(associated_data) + encryptor.finalize()

    return ciphertext

def aesdecrypt(key, ciphertext, associated_data=None):
    '''Decrypt ciphertext encrypted with AES in CBC mode.'''
    backend = default_backend()
    if associated_data is None:
        associated_data = b''

    cipher = Cipher(algorithms.AES(key), modes.CBC(bytes(16)), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    if associated_data:
        plaintext = decryptor.update(associated_data) + decryptor.finalize()

    #Remove padding
    plaintext = plaintext.decode('utf-8')  #Decode to string first
    padding_length = ord(plaintext[-1])
    plaintext = plaintext[:-padding_length]

    return plaintext

def blowfishencrypt(key, plaintext, mode=modes.CBC, iv=None):
    '''Encrypt plaintext using Blowfish in CBC mode.'''
    backend = default_backend()
    if iv is None:
        iv = bytes(8)

    #Pad the plaintext to a multiple of 8 bytes
    padding_length = 8 - (len(plaintext.encode('utf-8')) % 8)
    plaintext = plaintext + (chr(padding_length) * padding_length)

    cipher = Cipher(Blowfish(key), mode(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    return ciphertext

def blowfishdecrypt(key, ciphertext, mode=modes.CBC, iv=None):
    '''Decrypt ciphertext encrypted with Blowfish in CBC mode.'''
    backend = default_backend()
    if iv is None:
        iv = bytes(8)

    cipher = Cipher(Blowfish(key), mode(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    #Remove padding
    plaintext = plaintext.decode('utf-8')
    padding_length = ord(plaintext[-1])
    plaintext = plaintext[:-padding_length]

    return plaintext


#___Asymmetric Encryption___
def rsagenkey():
    '''Generate a new RSA key pair.'''
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def rsaencrypt(public_key, plaintext):
    '''Encrypt plaintext using an RSA public key.'''
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        PKCS1v15()
    )
    return ciphertext

def rsadecrypt(private_key, ciphertext):
    '''Decrypt ciphertext using an RSA private key.'''
    plaintext = private_key.decrypt(
        ciphertext,
        PKCS1v15()
    )
    return plaintext.decode('utf-8')


#___Hashing Algorithms___
def sha256(data):
    '''Calculate the SHA-256 hash of the given data.'''
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

def sha512(data):
    '''Calculate the SHA-512 hash of the given data.'''
    sha512 = hashlib.sha512()
    sha512.update(data.encode('utf-8'))
    return sha512.hexdigest()

def md5(data):
    '''Calculate the MD5 hash of the given data.'''
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()