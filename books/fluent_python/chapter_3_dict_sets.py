'''
    What is hashable?
        - An object is hashable if it has a hash value which never changes during its lifetime (it needs a __hash__() method), and can be compared to other objects 
        (it needs an __eq__() method)
        - User-defined types are hashable by default because their hash value is their id() and they all compare not equal. If an object implements a custom __eq__
        that takes into account its internal state, it may be hashable only if all its attributes are immutable
        -“All of Python's immutable built-in objects are hashable” with the exception of a tuple that contains mutable objects like lists

    Hashes and equality
        -  If two objects compare equal, their hash values must also be equal, otherwise the hash table algorithm does not work. For example, because
        1 == 1.0 is true, hash(1) == hash(1.0) must also be true, even though the internal representation of an int and a float are very different

    Default dicts:
        - They are configured to create items on demand whenever a missing key is searched
        - For example, if we have a dict set as dd = defaultdict(list), and we want to set a new key to the dict, the default value of that key will be a list

    Sets:
        - A collection of unique objects. The main usage of sets can be to remove duplicate values on lists 
        - Set elements must be hashable

'''
# You can check if an object is hashable or not by the following code
tt = (1, 2, (30, 40))
print(hash(tt))

# Example 1: How to build dicts using dict comps
DIAL_CODES = [ 
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan'),
]

country_code = {country: code for code, country in DIAL_CODES} 
print(country_code)
print({code: country.upper() for country, code in country_code.items() if code < 66})

# Using setdefault 
import sys
import re
WORD_RE = re.compile('\w+')
index = {}

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            # Get the list of occurences of that word, or if it doesn't exist yet, set to []
            # It is the same thing as using the code below, but in a efficient way (3 lines reduced to 1)
            # occurrences = index.get(word, []) 
            # occurrences.append(location) 
            # index[word] = occurrences 
            index.setdefault(word, []).append(location) 

for word in sorted(index, key=str.upper):
    print(word, index[word])

# Example 2: Creating default dicts
# This is the same problem as Example 1, but with a different solution - default dicts
import sys
import re
import collections
WORD_RE = re.compile('\w+')
index = collections.defaultdict(list) 

with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start()+1
            location = (line_no, column_no)
            index[word].append(location) 

for word in sorted(index, key=str.upper):
    print(word, index[word])

# Example 3: using set to count occurrences of needles in haystack
# Traditional way
HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
found = 0
for n in NEEDLES:
    if n in HAYSTACK:
        found += 1

# If they are both sets, the counting can be done on this way
found = len(NEEDLES & HAYSTACK)
found = len(set(NEEDLES) & set(HAYSTACK))

# Example 4: Building setcomps
from unicodedata import name 
{chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i),'')} 