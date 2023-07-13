#from pyetr import 

from typing import Callable


class stateset(frozenset):
    def atomic_answer_potential(self, other: "stateset") -> int:
        raise NotImplementedError
    
class Atom:
    name: str
    verifier: bool
    def __init__(self, name: str, verifier: bool = True) -> None:
        # ∈ Definition A1
        self.verifier = verifier
        self.name = name
    def __invert__(self):
        # Definition A1
        return Atom( self.name, not self.verifier)
    def __eq__(self, other):
        return (
        self.verifier == other.verifier
        ) and (
        self.name == other.name
        )
class State:
    def __init__(self, atoms: set[Atom]) -> None:
    # ∈ Definition A2
        self.atoms = atoms

class ArbitraryObject:
    def __init__(self, name: str) -> None:
        pass


class ArbitraryObjectSet:
    def __init__(self) -> None:
        self.i = 0
    def __next__(self):
        i +=1
        return ArbitraryObject(f"x{i}")
    def __iter__(self):
        return self
s = ArbitraryObjectSet()

x = "x"



class Action:
    def __init__(self, name:str, k:int) -> None:
        self.name = name

j = Action("john", 0)
a1 = Action("smokes", 1)
a2 = Action("loves", 2)

def john():
    return "john"
def mary():
    return "mary"
def smokes(person: str):
    return person + "_smokes"

def loves(person1: str, person2: str):
    return person1 + "_loves_" + person2
r1 = smokes(john())
r2 = loves(john(), mary())

Term = 
john_smokes = Atom("john_smokes")
mary_drinks = Atom("mary_drinks")
def test_predicate(arg1,arg2):
    pass
a = ("test_predicate", (1,2))

stateset({john_smokes, mary_drinks})

states = stateset({1,2}).atomic_answer_potential(stateset({3,4}))

G = View(set(frozenset(Smokes(John), Drinks(John)), frozenset(Smokes(Mary), Drinks(Mary)) ), set(frozenset()), (set(), set(), set()), set())

D = View(set(frozenset(Smokes(John))), set(frozenset()), (set(), set(), set()), set())

# Use the Answer method on G with D as an argument (see def A.40)

G_prime=G.Answer(D)

# G_prime would then evaluate to

View(set(frozenset(Smokes(John))), set(frozenset()), (set(), set(), set()), set())
