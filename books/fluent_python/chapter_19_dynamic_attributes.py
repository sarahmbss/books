'''
    Observations for the example 1:
        - When you code each property in the traditional way, the name of
        the attribute where you will store a value is hardcoded in the getter and setter methods.
        But here, the qty_getter and qty_setter functions are generic, and they depend on
        the storage_name variable to know where to get/set the managed attribute in the instance __dict__.
        - The functions qty_getter and qty_setter will be wrapped by the property object
        created in the last line of the factory function. Later when called to perform their duties,
        these functions will read the storage_name from their closures, to determine where to
        retrieve/store the managed attribute values.
        - the weight property overrides the
        weight instance attribute so that every reference to self.weight or nutmeg.weight is
        handled by the property functions

    Handling Attribute Deletion
        - In a property definition, the @my_propety.deleter decorator is used to wrap the 
        method in charge of deleting the attribute managed by the property

'''

# Example 1: Property Factory, in which the weight and product price can't be negative
class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price
    
def quantity(storage_name):
    def qty_getter(instance):
        return instance.__dict__[storage_name]
    
    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')
    return property(qty_getter, qty_setter)

# Example 2: Deleting a property attribute
class BlackKnight:
    def __init__(self):
        self.members = ['an arm', 'another arm','a leg', 'another leg']
        self.phrases = ["'Tis but a scratch.","It's just a flesh wound.","I'm invincible!","All right, we'll call it a draw."]

    @property
    def member(self):
        print('next member is:')
        return self.members[0]
    
    @member.deleter
    def member(self):
        text = 'BLACK KNIGHT (loses {})\n-- {}'
        print(text.format(self.members.pop(0), self.phrases.pop(0)))

    # It can also be done by using the following syntax (fdel)
    # member = property(member_getter, fdel=member_deleter)

