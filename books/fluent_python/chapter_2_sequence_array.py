'''
    Overview of built-in sequences

        Container sequences: 
            - list, tuple, collections 
            - holds items of different types
            - holds references to the objects they contain, which may be of any type

        Flat sequences: 
            - string, bytes, bytesarray, memory view 
            - holds items of one type
            - store the value of each item within its own memory space, and not as distinct objects 
            - limited to holding primitive values like characters, bytes, and numbers

        Mutable sequences:
            - list, bytearray, array.array, collections, memory view
            - has some features like insert, append, reverse, extend, pop that is not included on the immutable sequences
        
        Immutable sequences: 
            - tuple, str, and bytes

        Listcomp: 
            - is meant to do one thing only - build a new list
            - they work like functions, each variable inside the listcomp have their own local scope
            - they do everything the map and filter does, but they are easier to read

        Genexps:
            - Initializes tuples and arrays
            - Has the same syntax as listcomps, but with parentheses rather than brackets

        Tuples:
            - They can be used as immutable lists, but also as records with no field names
            - each item in the tuple holds the data for one field and the position of the item gives its meaning
            - Has the same attributes as a list (with the exception of those that add or remove elements)
            - Putting mutable items in tuples is not a good idea

        List:
            - The list.sort method sorts a list in place—that is, without making a copy
            - In contrast, the built-in function sorted creates a new list and returns it
            - If you are storing an 10 million floating-point values, an array is much more efficient
            - On the other hand, if you are constantly adding and removing items from the ends of a list as a FIFO or LIFO data structure, 
             a deque (double-ended queue) works faster
'''
# Example 1: Building a list of unicode codepoints from a string
symbols = '$¢£¥€¤'
codes = [ord(symbol) for symbol in symbols if ord(symbol) > 127]

# Example 1.1: the same as 1 but with map and filter 
example_map = list(filter(lambda c: c > 127, map(ord, symbols)))

# Example 2: Generating cartesian products using listcomp
colors = ['white', 'black']
sizes = ['S','M','L']
tshirts = [(color, size) for color in colors for size in sizes]

# Example 3: Generating the same output as example 1 but with genexps
symbols = '$¢£¥€¤'
codes = tuple(ord(symbol) for symbol in symbols if ord(symbol) > 127)

# Genexps can be used to save memory, as presented above
# If we were to use listcomp, they would build the items on memory and then use on the for loop
# As for genexps, the items are never built on memory, they feed the for loop producing one item at a time
# When we have milions of items we want to iterate on, genexps are better than listcomp
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)

# We can also use * to grab excess items 
a, b, *rest = range(5)

# Named tuples - easier to debug
from collections import namedtuple
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
tokyo.population

# Another way of using slicing
# We can name each slice, so that it'll be easier to debug later
invoice = """
0.....6.................................40........52...55........
1909 Pimoroni PiBrella $17.50 3 $52.50
1489 6mm Tactile Switch x20 $4.95 2 $9.90
1510 Panavise Jr. - PV-201 $28.00 1 $28.00
1601 PiTFT Mini Kit 320x240 $34.95 1 $34.95
"""
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
QUANTITY = slice(52, 55)
ITEM_TOTAL = slice(55, None)
line_items = invoice.split('\n')[2:]
for item in line_items:
    print(item[UNIT_PRICE], item[DESCRIPTION])

# A += Assignment Puzzler
# In the case below, the numbers 50 and 60 will be inserted to the list, but later, an error will apear on the screen
# This happens because t is an immutable object, that happens to have a mutable object
# In the end, despite the error at the end, t will be modified
t = (1, 2, [30, 40])
t[2] += [50, 60]

# Bisect does a binary search for needle in haystack—which must be a sorted sequence—to locate the position where needle can be inserted while maintaining 
# haystack in ascending order
import bisect
import sys
HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
ROW_FMT = '{0:2d} @ {1:2d} {2}{0:<2d}'

def demo(bisect_fn):
    ''' Para cada elemento dentro de needles, procura a posição de inserção dele para que a lista permaneça ordenada '''
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * ' |'
        print(ROW_FMT.format(needle, position, offset))

if __name__ == '__main__':
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
print('DEMO:', bisect_fn.__name__)
print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
demo(bisect_fn)

# Another usage for bisect is to insert a new item to a list, and keep it sorted
# Insort keeps a sorted sequence always sorted
import bisect
import random

SIZE = 7
random.seed(1729)
my_list = []

for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)




