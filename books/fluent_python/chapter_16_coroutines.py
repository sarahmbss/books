'''
    - It's crucial to understand that the execution of the coroutine is suspended exactly at the
    yield keyword
'''
# Example of coroutine
# The first activation of a coroutine is always done with next
def simple_coroutine(): # Defined as a generator function (yield on the body)
    print('-> coroutine started')
    x = yield 
    print('-> coroutine received:', x)