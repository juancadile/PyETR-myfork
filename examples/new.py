
from dataclasses import dataclass
from typing import AbstractSet, Iterable, Optional


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
    term: "Term | ArbitraryObject"
    def __init__(self, t: "Term | ArbitraryObject") -> None:
        self.term = t

class Term:
    f: Function
    t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]]
    has_emphasis: bool
    def __init__(self, f: Function, t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]] = None):
        if t is None and f.arity > 0:
            raise ValueError("Term not supplied when Function arity is greater than 0")
        elif t is not None and (len(t) != f.arity):
            raise ValueError(f"Term length {len(t)} did not match arity {f.arity}")
        self.f = f
        self.t = t
        if t is None:
            self.has_emphasis = False
        else:
            emphasis_count = self._count_emphasis(t)
            if emphasis_count > 1:
                raise ValueError(f"Emphasis in term with func: {self.f} greater than 1. Count: {emphasis_count})")
            else:
                self.has_emphasis = emphasis_count == 1

    @staticmethod
    def _count_emphasis(t: tuple["Term | ArbitraryObject | Emphasis", ...]) -> int:
        emphasis_count = 0
        for element in t:
            if isinstance(element, Emphasis):
                emphasis_count += 1
            elif isinstance(element, Term):
                emphasis_count += element.has_emphasis

        return emphasis_count

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
    predicate: Predicate
    terms: tuple[Term | ArbitraryObject | Emphasis,...]
    has_emphasis: bool
    def __init__(
        self, 
        predicate: Predicate, 
        terms: tuple[Term | ArbitraryObject | Emphasis,...]
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError("Inconsistent")
        self.predicate = predicate
        emphasis_count = 0
        for term in terms:
            if isinstance(term, Term):
                emphasis_count += term.has_emphasis
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in atom at: {emphasis_count}")
        else:
            self.has_emphasis = emphasis_count == 1
        self.terms = terms

        # Invarient: atom has one or 0 emphasis


class stateset(frozenset[Atom]):
    def __new__(cls, __iterable: Optional[Iterable[Atom]] = None, /) -> "stateset":
        if __iterable is None:
            return super().__new__(cls)
        else:
            return super().__new__(cls, __iterable)

    def copy(self) -> "stateset":
        return stateset(super().copy())
    def difference(self, *s: Iterable[object]) -> "stateset":
        return stateset(super().difference(*s))
    def intersection(self, *s: Iterable[object]) -> "stateset":
        return stateset(super().intersection(*s))
    def symmetric_difference(self, __s: Iterable[Atom]) -> "stateset":
        return stateset(super().symmetric_difference(__s))
    def union(self, *s: Iterable[Atom]) -> "stateset":
        return stateset(super().union(*s))
    def __and__(self, __value: AbstractSet[Atom]) -> "stateset":
        return stateset(super().__and__(__value))
    def __or__(self, __value: AbstractSet[Atom]) -> "stateset":
        return stateset(super().__or__(__value))
    def __sub__(self, __value: AbstractSet[Atom]) -> "stateset":
        return stateset(super().__sub__(__value))
    def __xor__(self, __value: AbstractSet[Atom]) -> "stateset":
        return stateset(super().__xor__(__value))


def get_arb_objects(states:stateset) -> tuple[set[ArbitraryObject], set[ArbitraryObject]]:
    raise NotImplementedError

def is_related(set1: set[ArbitraryObject], set2:set[ArbitraryObject]):
    return set1.issubset(set2) or set2.issubset(set1)

@dataclass
class Dependency:
    universal: ArbitraryObject
    existentials: set[ArbitraryObject]


def test_matroyshka(deps: set[Dependency]):
    existentials: list[set[ArbitraryObject]] = [
        d.existentials for d in deps
    ]
    stack = existentials.copy()
    while stack:
        compare_set1 = stack.pop(0)
        for compare_set2 in stack:
            if not is_related(compare_set1, compare_set2):
                raise ValueError(f'Existential sets do not meet Matroyshka condition. \nSet1: {compare_set1}\nSet2: {compare_set2}')



class DependencyRelation:
    dependencies: set[Dependency]

    def __init__(
        self, 
        dependencies: set[Dependency]
    ) -> None:
        test_matroyshka(dependencies)
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
        dependency_relation.validate(stage.union(supposition))
        self.dependency_relation = dependency_relation

        #view has exactly one emphasis

smokes = Predicate("smokes", 1)
existential_arb_set = ArbitraryObjectMaker(is_existential=True)
john_smokes = Atom(smokes, (Term(f=Function("john", 0)),))
existent_arb_obj = next(existential_arb_set)
arbitrary_object_smokes = Atom(smokes, (Emphasis(existent_arb_obj),))
