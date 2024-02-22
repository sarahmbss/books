'''
    Interfaces and Protocols in Python Culture
        - Even without an interface keyword in the language, and regardless of ABCs, every class has an
        interface: the set public attributes (methods or data attributes) implemented or inherited by the class
        - A useful complementary definition of interface is: the subset of an object's public methods that enable it 
        to play a specific role in the system
        - An interface seen as a set of methods to fulfill a role is what Smalltalkers called
        a procotol, and the term spread to other dynamic language communities
        - A class may implement several protocols, enabling its instances to fulfill several roles
        - Protocols are interfaces, but because they are informal - defined only by documentation
        and conventions - protocols cannot be enforced like formal interfaces can

    - ABCs are meant to encapsulate very general concepts, abstractions, introduced by a
    framework—things like “a sequence” and “an exact number.” [Readers] most likely don't
    need to write any new ABCs, just use existing ones correctly, to get 99.9% of the benefits
    without serious risk of misdesign
'''