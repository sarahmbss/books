'''
    Introduction
        - An encoding is an algorithm that converts code points to byte sequences and vice versa.
        - Converting from code points to bytes is encoding
        - Converting from bytes to code points is decoding

    Byte Essentials
        - For bytes in the printable ASCII range—from space to ~—the ASCII character itself is used
        - For bytes corresponding to tab, newline, carriage return, and \, the escape sequences \t, \n, \r, and \\ are used
        - For every other byte value, a hexadecimal escape sequence is used (e.g., \x00 is the null byte)
        - Both bytes and bytearray support every str method except those that do formatting (format, format_map) and a few others that depend on Unicode data
        - In addition, the regular expression functions in the re module also work on binary sequences, if the regex is compiled from a binary sequence instead of a str
    
    Structs and Memory Views
        - The struct module provides functions to parse packed bytes into a tuple of fields of different types and to perform the opposite conversion, 
        from a tuple into packed bytes
        - The memoryview class does not let you create or store byte sequences, but provides shared memory access to slices of data from
        other binary sequences, packed arrays, and buffers such as Python Imaging Library (PIL) images, 2 without copying the bytes

    Basic Encoders/Decoders
        - The UTF encodings, however, are designed to handle every Unicode code point
        - Latin1: the basis for other encodings, such as cp1252 and Unicode itself -- same as iso8859_1
        - cp1252: A latin1 superset by Microsoft, adding useful symbols like curly quotes and the € (euro)
        - cp437: The original character set of the IBM PC, with box drawing characters. Incompatible with latin1, which appeared later
        - utf8: The most common 8-bit encoding on the Web, by far;3 backward-compatible with ASCII

    Understanding Encode/Decode Problems
        - Most non-UTF codecs handle only a small subset of the Unicode characters. When converting text to bytes, if a character is not 
        defined in the target encoding, UnicodeEncodeError will be raised
        - Sometimes you can get an error of encode, when opening .py files. Because UTF-8 is widely deployed in GNU/Linux and OSX systems, a likely scenario
        is opening a .py file created on Windows with cp1252. Note that this error happens even in Python for Windows, because the 
        default encoding for Python 3 is UTF-8 across all platforms

    How to Discover the Encoding of a Byte Sequence
        - Some communication protocols and file formats, like HTTP and XML, contain headers that explicitly tell us how the content is encoded
        - Chardet is a Python library that you can use in your programs, but also includes a command-line utility, chardetect
        - On linux, you can also check the enconding with the line: file file.txt for example

    Handling Text Files
        - The best practice for handling text is the “Unicode sandwich”: 
            -- Decode bytes on input (bytes -> str)
            -- Process text 100% on str
            -- Encode text on output
        - Code that has to run on multiple machines or on multiple occasions should never depend on encoding defaults. Always pass an
        explicit encoding = argument when opening text files, because the default may change from one machine to the next, or from one day to the next
    
    Sorting Unicode Text
    - Python sorts sequences of any type by comparing the items in each sequence one by one. For strings, this means comparing the code points.
    Unfortunately, this produces unacceptable results for anyone who uses non-ASCII characters

'''

# Exemplo 1: Diferentes representações de uma string em encodes diferentes
# Bytes literals start with a b prefix, that is why the result shows a b at the beginning
# Here the letter é with an accent is shown that way because it is not in the printable ASCII range
print('café'.encode('ISO-8859-1'))
print('café'.encode('utf-8'))
print('café'.encode('cp1252'))

# The code point U+0301 is the COMBINING ACUTE ACCENT. Using it after “e” renders “é”.
# In the Unicode standard, sequences like 'é' and 'e\u0301' are called “canonical equiv‐
# alents,” and applications are supposed to treat them as the same. But Python sees two
# different sequences of code points, and considers them not equal
s1 = 'café'
s2 = 'cafe\u0301'
print(len(s1), len(s2))
print(s1 == s2)

# The answer on this case is to normalize the words 
# NFC composes the code points to produce the shortest equivalent string
# NFD decomposes, expanding composed characters into base characters and separate combining characters
from unicodedata import normalize
s1 = 'café' # composed "e" with acute accent
s2 = 'cafe\u0301' # decomposed "e" and acute accent
print(len(s1), len(s2))
print(len(normalize('NFC', s1)), len(normalize('NFC', s2)))
print(len(normalize('NFD', s1)), len(normalize('NFD', s2)))
print(normalize('NFC', s1) == normalize('NFC', s2))


# Function to remove all combining marks
# Sometimes this piece of code will generate a couple of errors, because it can normalize greek letters in a wrong way
import unicodedata
import string
def shave_marks(txt):
    """Remove all diacritic marks"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt
    if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)

order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
print(shave_marks(order))

# This function solves the error caused by the previous one
def shave_marks_latin(txt):
    """Remove all diacritic marks from Latin base characters"""
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue
        keepers.append(c)
        # if it isn't combining char, it's a new base char
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

# Sorting unicode text
# Using the locale.strxfrm function as sort key
# This will ignore the accents when sorting the list
# This solution has many set backs such as th fact that is not good to set locale 
# The locale must be correctly implemented by the makers of the OS
import locale
locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=locale.strxfrm)
print(sorted_fruits)

import pyuca
coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)