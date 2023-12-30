
'''
    As the strategy methods have no state, they could also be implemented as plain functions, without the abstract class Promotion
    
    But often concrete strategies have no internal state; they only deal with data from the context. If that is the
    case, then by all means use plain old functions instead of coding single-method classes
    implementing a single-method interface declared in yet another class. A function is
    more lightweight than an instance of a user-defined class, and there is no need for
    Flyweight because each strategy function is created just once by Python when it compiles
    the module. A plain function is also “a shared object that can be used in multiple contexts
    simultaneously.”

'''


# Example of the usage of the classic strategy
from abc import ABC, abstractmethod
from collections import namedtuple
import inspect
Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity
    
class Order: 
    """ The Context: Provides a service by delegating some computation to interchangeable components
        that implement alternative algorithms """
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
    
class Promotion(ABC): 
    """ The Strategy: The interface common to the components that implement the different algorithms """
    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount"""

class FidelityPromo(Promotion): # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0
    
class BulkItemPromo(Promotion): # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount

# The module globals return a dictionary representing the current global symbol table  
# This is always the dictionary of the current module (inside a function or method, this is the module where it is defined, not the module from which it is called)
# That way we can catch all the functions that ends with promo without having any other kind of control of the discounts we have
promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo'] 

# Another way of getting the promo functions would be to place them inside a class and then inspecting the modules of that class
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]