'''
    Subclassing Built-In Types Is Tricky
        - Before Python 2.2, it was not possible to subclass built-in types such as list or dict.
        Since then, it can be done but there is a major caveat: the code of the built-ins (written
        in C) does not call special methods overridden by user-defined classes.
        - This built-in behavior is a violation of a basic rule of object-oriented programming: the
        search for methods should always start from the class of the target instance (self), even
        when the call happens inside a method implemented in a superclass
        - Subclassing built-in types like dict or list or str directly is errorprone because the built-in 
        methods mostly ignore user-defined overrides.
        - Instead of subclassing the built-ins, derive your classes
        from the collections module using UserDict, UserList, and
        UserString, which are designed to be easily extended.

    Multiple Inheritance and Method Resolution Order
        - Python follows a specific order
        when traversing the inheritance graph. That order is called MRO: Method Resolution
        Order. Classes have an attribute called __mro__ holding a tuple of references to the
        superclasses in MRO order, from the current class all the way to the object class
        - The MRO takes into account not only the inheritance graph but also the order in which
        superclasses are listed in a subclass declaration. The first one you declare, will also be the first one linked.

    Coping with Multiple Inheritance
        1. Distinguish Interface Inheritance from Implementation Inheritance
            The main reasons why subclassing is used are:
                • Inheritance of interface creates a subtype, implying an “is-a” relationship.
                • Inheritance of implementation avoids code duplication by reuse.
        2. Make Interfaces Explicit with ABCs
            In modern Python, if a class is designed to define an interface, it should be an explicit ABC
        3. Use Mixins for Code Reuse
            If a class is designed to provide method implementations for reuse by multiple unrelated
            subclasses, without implying an “is-a” relationship, it should be an explicit mixin class.
        4. Make Mixins Explicit by Naming
            There is no formal way in Python to state that a class is a mixin, so it is highly recommended that they 
            are named with a …Mixin suffix
        5. An ABC May Also Be a Mixin; The Reverse Is Not True
            Because an ABC can implement concrete methods, it works as a mixin as well. An ABC
            also defines a type, which a mixin does not. One restriction applies to ABCs and not to mixins: the concrete methods implemented
            in an ABC should only collaborate with methods of the same ABC and its superclasses.
        6. Don't Subclass from More Than One Concrete Class
            Concrete classes should have zero or at most one concrete superclass
        7. Provide Aggregate Classes to Users
            If some combination of ABCs or mixins is particularly useful to client code, provide a
            class that brings them together in a sensible way
        8. “Favor Object Composition Over Class Inheritance.”
            Once you get comfortable with inheritance, it's too easy to overuse it. However, favoring composition leads to more flexible designs.
'''

# Example 1:  Our __setitem__ override is ignored by the __init__ and __update__ methods of the built-in dict
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2) # duplicates values when storing, it works by delegating to the superclass

dd = DoppelDict(one=1) # The __init__ method inherited from dict clearly ignored that __setitem__ was overridden: the value of 'one' is not duplicated
print(dd)
dd['two'] = 2 # The [] operator calls our __setitem__ and works as expected: 'two' maps to the duplicated value [2, 2]
print(dd)

# Example 2: The corret way of subclassing built-in types
import collections
class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

# all values are duplicated, just as they should be
dd = DoppelDict2(one=1)
print(dd)
dd['two'] = 2
print(dd)