'''
    Why Sequences Are Iterable: The iter Function
        - Whenever the interpreter needs to iterate over an object x, it automatically calls iter(x)
        - The iter built-in function:
            1. Checks whether the object implements __iter__, and calls that to obtain an iterator.
            2. If __iter__ is not implemented, but __getitem__ is implemented, Python creates -- this is why any python sequence is iterable
            an iterator that attempts to fetch items in order, starting from index 0 (zero).
            3. If that fails, Python raises TypeError, usually saying “C object is not iterable,” where
            C is the class of the target object.

    Iterables Versus Iterators
        - iterable: Any object from which the iter built-in function can obtain an iterator. Objects
        implementing an __iter__ method returning an iterator are iterable. Sequences
        are always iterable; as are objects implementing a __getitem__ method that takes 0-based indexes
        - Python obtains iterators from iterables
        - iterator: Any object that implements the __next__ no-argument method that returns the
        next item in a series or raises StopIteration when there are no more items. Python
        iterators also implement the __iter__ method so they are iterable as well.

    The standard interface for an iterator has two methods:
        __next__: Returns the next available item, raising StopIteration when there are no more items
        __iter__: Returns self; this allows iterators to be used where an iterable is expected, for example, in a for loop.

    Generator Expressions: When to use them
        - On the other hand, generator functions are much more flexible: you can code complex logic with multiple statements, and
        can even use them as coroutines
        - Generator functions have a name, so they can be reused. You can
        always name a generator expression and use it later by assigning it to a variable, of course,
        but that is stretching its intended usage as a one-off generator
            

'''
print(list('teste para ver'))

# Check if an object is iterable or not
print(iter('teste'))

# Example of an iterator
class Iterator(Iterable):
    __slots__ = ()

    @abstractmethod
    def __next__(self):
        'Return the next item from the iterator. When exhausted, raise StopIteration'
        raise StopIteration
    
    def __iter__(self):
        return self
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and any("__iter__" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented

# Example of filtering generator functions
def vowel(c):
    return c.lower() in 'aeiou'
list(filter(vowel, 'Aardvark'))

import itertools
print(list(itertools.filterfalse(vowel, 'Aardvark')))
print(list(itertools.dropwhile(vowel, 'Aardvark')))
print(list(itertools.takewhile(vowel, 'Aardvark')))
print(list(itertools.compress('Aardvark', (1,0,1,1,0,1))))
print(list(itertools.islice('Aardvark', 4)))
print(list(itertools.islice('Aardvark', 4, 7)))
print(list(itertools.islice('Aardvark', 1, 7, 2)))

# Example of acummulate generator functions
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
import itertools
print(list(itertools.accumulate(sample)))
print(list(itertools.accumulate(sample, min))) 
print(list(itertools.accumulate(sample, max))) 

# Example of mapping generator functions
print(list(enumerate('albatroz', 1))) 
import operator
print(list(map(operator.mul, range(11), range(11)))) 
print(list(map(operator.mul, range(11), [2, 4, 8]))) 
print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))
