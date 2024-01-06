'''
    classmethod Versus staticmethod
        - classmethod:  to define a method that operates
        on the class and not on instances. classmethod changes the way the method is called,
        so it receives the class itself as the first argument, instead of an instance
        - By convention, the first parameter of a class method should be named cls 
        - staticmethod decorator changes a method so that it receives no special first argument
        - a static method is just like a plain function that happens to live in a class body, instead of being defined at the module level
        - Basically both of them allows us to call the methods inside a class without calling the class itself. The difference
        if that classmethod can also be used to pass objects from a different class or itself

    Private and “Protected” Attributes in Python
        - In Python, there is no way to create private variables like there is with the private
        modifier in Java. What we have in Python is a simple mechanism to prevent accidental
        overwriting of a “private” attribute in a subclass
        - if you name an instance attribute in the form __mood (two leading
        underscores and zero or at most one trailing underscore), Python stores the name in
        the instance __dict__ prefixed with a leading underscore and the class name
        - Attributes with a single _ prefix are called “protected” in some corners of the Python documentation. The practice of “protecting” 
        attributes by convention with the form self._x is widespread, but calling that a “protected” attribute is not so common. Some
        even call that a “private” attribute

    Saving Space with the __slots__ Class Attribute
        - By default, Python stores instance attributes in a per-instance dict named __dict__
        - To summarize, __slots__ has some caveats and should not be abused just for the sake
        of limiting what attributes can be assigned by users. It is mostly useful when working
        with tabular data such as database records where the schema is fixed by definition and
        the datasets may be very large
        - If your program is not handling millions of instances, it's probably not worth the trouble
        of creating a somewhat unusual and tricky class whose instances may not accept dynamic attributes or may not support weak references
        
'''
# Example 1: How to use staticmethod
class Escritor():
    def __init__(self):
        pass

    def escreve(self, text):
        print(text)

    @staticmethod
    def escreve_novo(text):
        print(text)

Escritor.escreve_novo("Olá!")

# Example 2: How to use classmethod
class Pessoa():
    def __init__(self, altura, idade):
        self.altura = altura
        self.idade = idade

class Aluno():
    def __init__(self, altura, idade):
        self.altura = altura
        self.idade = idade

    @classmethod
    # Here we are using the class Pessoa to create a person that is at the same time, student
    def construir_aluno_pessoa(cls, pessoa):
        return cls(pessoa.altura, pessoa.idade)

    def estudar(self):
        print("Estou estudando")

joao = Pessoa(1.85, 18)
mariaAluna = Aluno(1.68, 18)
mariaAluna.estudar()

joaoAluno = Aluno.construir_aluno_pessoa(joao)
joaoAluno.estudar()

# Example 3: adding slots attributes to a class
# By defining __slots__ in the class, you are telling the interpreter: “These are all the
# instance attributes in this class.”
class Vector2d:
    __slots__ = ('__x', '__y')
    typecode = 'd'
