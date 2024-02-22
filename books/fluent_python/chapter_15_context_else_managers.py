'''
    Context Managers and else Blocks
        - The with statement sets up a temporary context and reliably tears it down, under the
        control of a context manager object. This prevents errors and reduces boilerplate code,
        making APIs at the same time safer and easier to use

    Do This, Then That: else Blocks Beyond if
        - This is no secret, but it is an underappreciated language feature: the else clause can be
        used not only in if statements but also in for, while, and try statements.
        - for: The else block will run only if and when the for loop runs to completion (i.e., not
        if the for is aborted with a break).
        - while: The else block will run only if and when the while loop exits because the condition
        became falsy (i.e., not when the while is aborted with a break).
        - try: The else block will only run if no exception is raised in the try block. The official
        docs also state: “Exceptions in the else clause are not handled by the preceding
        except clauses.”
        - In the case of try/except blocks, else may seem redundant at first. After all, the
        after_call() in the following snippet will run only if the dangerous_call() does not
        raise an exception, correct? However, doing so puts the after_call() inside the try block for no good reason. For
        clarity and correctness, the body of a try block should only have the statements that
        may generate the expected exceptions

    Context Managers and with Blocks
        - The with statement was designed to simplify the try/finally pattern, which guarantees
        that some operation is performed after a block of code, even if the block is aborted
        because of an exception, a return or sys.exit() call. The code in the finally clause
        usually releases a critical resource or restores some previous state that was temporarily
        changed.

    Using @contextmanager
        - The @contextmanager decorator reduces the boilerplate of creating a context manager:
        instead of writing a whole class with __enter__/__exit__ methods, you just implement
        a generator with a single yield that should produce whatever you want the __en
        ter__ method to return
        - In a generator decorated with @contextmanager, yield is used to split the body of the
        function in two parts: everything before the yield will be executed at the beginning of
        the while block when the interpreter calls __enter__; the code after yield will run
        when __exit__ is called at the end of the block
'''
# Example of else on a for loop
my_list=['banana','apple']
for item in my_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')

# Example of else on a try block
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()

# Example of a context manager
from mirror import LookingGlass
with LookingGlass() as what: #The context manager is an instance of LookingGlass. Python calls __enter__ on the context manager and the result is bound to what
    print('Alice, Kitty and Snowdrop')
    print(what)
# The context is over
    
import contextlib
@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    def reverse_write(text):
        original_write(text[::-1])
    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY' # Yield the value that will be bound to the target variable in the as clause of the with statement. This function pauses at this point while the body of the with executes.
    sys.stdout.write = original_write # When control exits the with block in any way, the original is restored
