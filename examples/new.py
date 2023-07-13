from ast import Tuple
from copy import copy
from dataclasses import dataclass
from typing import Optional, overload

from numpy import issubsctype



class Function:
    name: str
    arity: int
    def __init__(self,name: str,arity: int) -> None:
        if arity < 0:
            raise ValueError("arity must be greater than 0")
        self.name = name
        self.arity = arity
    def __repr__(self) -> str:
        return f"Function({self.name}, {self.arity})"

    def get_term(self, *args):
        if len(args) == 0:
            return (self,)
        else:
            return (self, args)

class ArbitraryObject:
    name: str
    is_existential: bool
    def __init__(self, name: str, is_existential: bool):
        self.name = name
        self.is_existential = is_existential

class Term:
    def __init__(self, f: Function, t: Optional[tuple["Term | ArbitraryObject"]] = None):
        if t is None and f is not None and f.arity > 0:
            raise ValueError("Inconsistent")
        self.f = f
        self.t = t

# Changed if clause in 4.2 to separate Arbitrary Objects from Term



class ArbitraryObjectMaker:
    def __init__(self, is_existential: bool) -> None:
        self.i = 0
        self.is_existential = is_existential
    def __next__(self):
        self.i +=1
        return ArbitraryObject(name=f"x{self.i}", is_existential=self.is_existential)
    def __iter__(self):
        return self

class QuestionMark:
    def __repr__(self) -> str:
        return f"QuestionMark()"

question_mark_set = {QuestionMark()}

# Objects need to be managed
class Predicate:
    name: str
    verifier: bool
    arity: int
    def __init__(self, name: str, arity: int, _verifier: bool = True) -> None:
        self.verifier = _verifier
        self.name = name
        self.arity = arity
    def __invert__(self):
        return Predicate( self.name, not self.verifier)

equals_p = Predicate("=", 2)



class Atom:
    def __init__(self, predicate: Predicate, terms: tuple[Term | ArbitraryObject]) -> None:
        if len(terms) != predicate.arity:
            raise ValueError("Inconsistent")
        self.predicate = predicate
        self.terms = terms


class stateset(frozenset[Atom]):
    def __init__(self, atoms: set[Atom]) -> None:
        self.atoms = atoms

def get_arb_objects(states:stateset) -> tuple[set[ArbitraryObject], set[ArbitraryObject]]:
    raise NotImplementedError

def is_related(set1: set[ArbitraryObject], set2:set[ArbitraryObject]):
    return set1.issubset(set2) or set2.issubset(set1)

@dataclass
class Dependency:
    universal: ArbitraryObject
    existentials: set[ArbitraryObject]


def compare_existentials(deps: set[Dependency]):
    existentials: list[set[ArbitraryObject]] = [
        d.existentials for d in deps
    ]
    #compare any two sets of existentials, with is_related
    raise NotImplementedError
    # stack = copy(existentials)
    # while stack:
    #     ext1 = stack.pop(0)
    # for e1 in existentials:





class DependencyRelation:
    dependencies: set[Dependency]

    def __init__(
        self, 
        states: stateset, 
        dependencies: set[Dependency]
    ) -> None:
        uni_arb_objects, exi_arb_objects = get_arb_objects(states)
        # universal to existentials that depend on them ( share a pair )
        for d in dependencies:
            if d.existentials.issubset(exi_arb_objects):
                raise ValueError(f"{d.existentials} not found in states")
            if d.universal not in uni_arb_objects:
                raise ValueError(f"{d.universal } not found in states")
        compare_existentials(dependencies)

        self.dependencies = dependencies

class dependency_relations:
    def __init__(self, deps: set[DependencyRelation]) -> None:
        pass


smokes = Predicate("smokes", 1)
existential_arb_set = ArbitraryObjectMaker(is_existential=True)
john_smokes = Atom(smokes, (Term(f=Function("john", 0)),))
existent_arb_obj = next(existential_arb_set)
arbitrary_object_smokes = Atom(smokes, (existent_arb_obj,))
