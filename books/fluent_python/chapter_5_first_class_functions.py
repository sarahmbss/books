'''
    Functions in Python are first class objects:
        - They are created at runtime
        - Assigned to a variable or element in a data structure
        - Passed as an argument to a function
        - Returned as the result of a function

    Higher-Order Functions
        - A function that takes a function as argument or returns a function as the result is a higher-order function.

    Modern replacements for map, filter, reduce
        - The map and filter functions are still builtins in Python 3, but since the introduction of list comprehensions and generator expressions, 
        they are not as important. A listcomp or a genexp does the job of map and filter combined, but is more readable

    Anonymous Functions
        - The lambda keyword creates an anonymous function within a Python expression
        - The body of a lambda cannot make assignments or use any other Python statement such as while, try
        - A lambda expression creates a function object just like the def statement

    User-Defined Callable Types
        - A class implementing __call__ is an easy way to create function-like objects that have some internal state that must be kept across invocations
        - An example is a decorator. Decorators must be functions, but it is sometimes convenient to be able to “remember” something between calls of the decorator

'''

# Example 1: Using function as an argument of another function
# On this case, factorial is an argument of the function map
def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n-1)
print(map(factorial, range(11)))

# Another example is the function sorted, which allows you to provide a function to be applied to each item for sorting, through the item key
# Any one-argument function can be used as the key
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=len))

# The same example above, but using lambda to order by the last letter
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=lambda word: word[::-1]))

# Listcomp vs map/filter
print(list(map(factorial, filter(lambda n: n % 2, range(6)))))
print([factorial(n) for n in range(6) if n % 2])

### User-Defined Callable Types
import random
class BingoCage:
    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    # It is a shortcut to bingo.pick()
    def __call__(self):
        return self.pick()

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
bingo = BingoCage(range(3))
# Both lines above produce the same result
print(bingo.pick())
print(bingo())

# Example: Usage of itemgetter 
# Sorts the list based on the first argument of the tuple
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
from operator import itemgetter
for city in sorted(metro_data, key=itemgetter(1)):
    print(city)

# Example: Usage of attrgetter
from collections import namedtuple
LatLong = namedtuple('LatLong', 'lat long') 
Metropolis = namedtuple('Metropolis', 'name cc pop coord')
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long)) for name, cc, pop, (lat, long) in metro_data]
print(metro_areas[0].coord.lat)

from operator import attrgetter
name_lat = attrgetter('name', 'coord.lat') #Define an attrgetter to retrieve the name and the coord.lat nested attribute
for city in sorted(metro_areas, key=attrgetter('coord.lat')): #Use attrgetter again to sort list of cities by latitude
    print(name_lat(city)) #Use the attrgetter defined to show only city name and latitude

    


