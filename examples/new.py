
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar




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

class Emphasis:
    def __init__(self, t: "Term | ArbitraryObject") -> None:
        pass


class Term:
    def __init__(self, f: Function, t: Optional[tuple["Term | ArbitraryObject | Emphasis"]] = None):
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
    def __init__(
        self, 
        predicate: Predicate, 
        terms: tuple[Term | ArbitraryObject | Emphasis,...]
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError("Inconsistent")
        self.predicate = predicate
        self.terms = terms
        #atom has one or 0 emphasis

T = TypeVar("T", bound=set)
class stateset(frozenset[T], Generic[T]):
    def __init__(self, atoms: set[T] | frozenset[T]) -> None:
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
        dependencies: set[Dependency]
    ) -> None:
        compare_existentials(dependencies)

        self.dependencies = dependencies
    def validate(self, states: stateset):
        uni_arb_objects, exi_arb_objects = get_arb_objects(states)
        # universal to existentials that depend on them ( share a pair )
        for d in self.dependencies:
            if d.existentials.issubset(exi_arb_objects):
                raise ValueError(f"{d.existentials} not found in states")
            if d.universal not in uni_arb_objects:
                raise ValueError(f"{d.universal } not found in states")

class View:
    stage: stateset
    supposition: stateset
    dependency_relation: DependencyRelation

    def __init__(
        self, 
        stage: stateset, 
        supposition: stateset, 
        dependency_relation: DependencyRelation
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        dependency_relation.validate(stateset(stage.union(supposition)))
        self.dependency_relation = dependency_relation

        #view has exactly one emphasis

smokes = Predicate("smokes", 1)
existential_arb_set = ArbitraryObjectMaker(is_existential=True)
john_smokes = Atom(smokes, (Term(f=Function("john", 0)),))
existent_arb_obj = next(existential_arb_set)
arbitrary_object_smokes = Atom(smokes, (Emphasis(existent_arb_obj),))





