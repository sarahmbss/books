'''
    Sumary
        - Every Python object has an identity, a type, and a value. Only the value of an object changes over time
        - In Python, the function gets a copy of the arguments, but the arguments are always references

    Function Parameters as References
        - The only mode of parameter passing in Python is call by sharing. Call by sharing means that each formal
        parameter of the function gets a copy of each reference in the arguments. In other words, the parameters inside the function 
        become aliases of the actual arguments.
    
    del and Garbage Collection
        - Objects are never explicitly destroyed; however, when they become unreachable they may
        be garbage-collected
        - The del statement deletes names, not objects. An object may be garbage collected as
        result of a del command, but only if the variable deleted holds the last reference to the
        object, or if the object becomes unreachable

    Weak References
        - The presence of references is what keeps an object alive in memory. When the reference
        count of an object reaches zero, the garbage collector disposes of it. But sometimes it is
        useful to have a reference to an object that does not keep it around longer than necessary. A common use case is a cache.
        - Weak references are useful in caching applications because you don't want the cached
        objects to be kept alive just because they are referenced by the cache    
'''

# Example 1: A function may change any mutable object it receives
def f(a, b):
    a += b
    return a

x = 1
y = 2
print(f(x, y))
print(x, y) # Here, the number x is unchanged

a = [1, 2]
b = [3, 4]
print(f(a, b))
print(a, b) # Here the list a is changes

# Example 2: Defensive Programming with Mutable Parameters
# his assignment makes self.passengers an alias for passengers,
# which is itself an alias for the actual argument passed to __init__. That way, any change we make to passengers inside the class, 
# will be reflected on basketball_team
class TwilightBus:
    """A bus model that makes passengers vanish"""
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers # to fix this, we can make a copy using list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
print(basketball_team)

# Example 4: A weak reference is a callable that returns the referenced object or None if the referent is no more
# In practice, most of the time Python programs use the weakref collections
import weakref
a_set = {0, 1}
wref = weakref.ref(a_set)
print(wref)
print(wref()) # Invoking wref() returns the referenced object

a_set = {2, 3, 4}
print(wref())
print(wref() is None)
print(wref() is None)