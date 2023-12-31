"""
    - Function decorators let us “mark” functions in the source code to enhance their behavior in some way
    - A decorator is a callable that takes another function as argument (the decorated function).2 The decorator may perform some processing 
    with the decorated function, and returns it or replaces it with another function or callable object.

    Crucial Facts:
    -  They have the power to replace the decorated function with a different one
    -  They are executed immediately when a module is loaded (usually at import time)

    Closure
    - A closure is a function with an extended scope that encompasses nonglobal
    variables referenced in the body of the function but not defined there
"""
print('------ Running example 1')
# A decorator usually replaces a function with a different one
def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

# Invoking the decorated target actually runs inner
target()

# Example 2:  function decorators are executed as soon as the module is imported, but the decorated functions only run when they are explicitly invoked
# This example is unusual because:
# - A real decorator is usually defined in one module and applied to functions in other modules
# - In practice, most decorators define an inner function and return it (the same as example above)
print('\n ------ Running example 2')
registry = []
def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__=='__main__':
    main()

# Example 3: Using decorators to add the promo functions to a list (example used on the previous chapter)
# Any function decorated by @promotion will be added to promos
print('\n ------ Running example 3')
promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promo_func

@promotion
def fidelity(order):
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item(order):
    """10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion
def large_order(order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    """Select best discount available """
    return max(promo(order) for promo in promos)

# Example 4: Implementing a simple decorator
print('\n ------ Running example 4')
import time
import functools

def clock(func):
    @functools.wraps(func) #copy the relevant attributes from func to clocked
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked

# Using the clock decorator
# This is the typical behavior of a decorator: it replaces the decorated function with a new
# function that accepts the same arguments and (usually) returns whatever the decorated
# function was supposed to return, while also doing some extra processing
import time

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))

# Example 5: Using caching for faster implementation of recursive functions
# That way, the function is called only once for each value of n
print('\n ------ Running example 5')
@functools.lru_cache() 
@clock 
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    print(fibonacci(6))

# Example 6: using single dispatch to call specialized functions
# If you decorate a plain function with @singledispatch,
# it becomes a generic function: a group of functions to perform the same operation in
# different ways, depending on the type of the first argument
print('\n ------ Running example 6')
from functools import singledispatch
import numbers
import html

@singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)

@htmlize.register(str)
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)

@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)

# Example 7: Parametrized decorators
# Check if the function is active or not
registry = set()
def register(active=True):
    def decorate(func):
        print('running register(active=%s)->decorate(%s)'
        % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate

@register(active=False)
def f1():
    print('running f1()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1()

if __name__=='__main__':
    main()