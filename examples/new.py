from pprint import pformat
from typing import AbstractSet, Iterable, Optional


class Function:
    name: str
    arity: int

    def __init__(self, name: str, arity: int) -> None:
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

    def __repr__(self) -> str:
        return f"<ArbitraryObject name={self.name}"


class Emphasis:
    term: "Term | ArbitraryObject"

    def __init__(self, t: "Term | ArbitraryObject") -> None:
        self.term = t

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        subterm = self.term
        if isinstance(subterm, Term):
            output_set |= subterm.arb_objects
        elif isinstance(subterm, ArbitraryObject):
            output_set.add(subterm)
        else:
            assert False
        return output_set

    def __repr__(self) -> str:
        return f"<Emphasis term={self.term}>"


class Term:
    f: Function
    t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]]
    has_emphasis: bool

    def __init__(
        self,
        f: Function,
        t: Optional[tuple["Term | ArbitraryObject | Emphasis", ...]] = None,
    ):
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
                raise ValueError(
                    f"Emphasis in term with func: {self.f} greater than 1. Count: {emphasis_count})"
                )
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

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_set = set()
        if self.t is None:
            return output_set
        else:
            for term in self.t:
                if isinstance(term, Term) or isinstance(term, Emphasis):
                    output_set |= term.arb_objects
                elif isinstance(term, ArbitraryObject):
                    output_set.add(term)
                else:
                    assert False
            return output_set

    def __repr__(self) -> str:
        return f"<Term f={self.f} t={self.t}>"


# Changed if clause in 4.2 to separate Arbitrary Objects from Term


class ArbitraryObjectMaker:
    def __init__(self, is_existential: bool) -> None:
        self.i = 0
        self.is_existential = is_existential

    def __next__(self):
        self.i += 1
        return ArbitraryObject(name=f"x{self.i}", is_existential=self.is_existential)

    def __iter__(self):
        return self


class Predicate:
    name: str
    verifier: bool
    arity: int

    def __init__(self, name: str, arity: int, _verifier: bool = True) -> None:
        self.verifier = _verifier
        self.name = name
        self.arity = arity

    def __invert__(self):
        return Predicate(self.name, not self.verifier)

    def __repr__(self) -> str:
        return f"<Predicate name={self.name}"


equals_p = Predicate("=", 2)


class Atom:
    predicate: Predicate
    terms: tuple[Term | ArbitraryObject | Emphasis, ...]
    has_emphasis: bool

    def __init__(
        self, predicate: Predicate, terms: tuple[Term | ArbitraryObject | Emphasis, ...]
    ) -> None:
        if len(terms) != predicate.arity:
            raise ValueError("Inconsistent")
        self.predicate = predicate
        emphasis_count = 0
        for term in terms:
            if isinstance(term, Term):
                emphasis_count += term.has_emphasis
            elif isinstance(term, Emphasis):
                emphasis_count += 1
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in atom at: {emphasis_count}")
        else:
            self.has_emphasis = emphasis_count == 1
        self.terms = terms

        # Invarient: atom has one or 0 emphasis

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        output_objs = set()
        for term in self.terms:
            if isinstance(term, Term) or isinstance(term, Emphasis):
                output_objs |= term.arb_objects
            elif isinstance(term, ArbitraryObject):
                output_objs.add(term)
            else:
                assert False
        return output_objs

    def __repr__(self) -> str:
        return f"<Atom predicate={self.predicate} terms={self.terms}>"


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

    @property
    def arb_objects(self) -> set[ArbitraryObject]:
        arb_objects: set[ArbitraryObject] = set()
        for atom in self:
            arb_objects |= atom.arb_objects
        return arb_objects

    @property
    def has_emphasis(self) -> bool:
        emphasis_count = 0
        for atom in self:
            emphasis_count += atom.has_emphasis
        if emphasis_count > 1:
            raise ValueError(f"Emphasis count in stateset at: {emphasis_count}")
        else:
            return emphasis_count == 1


class Dependency:
    universal: ArbitraryObject
    existentials: frozenset[ArbitraryObject]

    def __init__(
        self, universal: ArbitraryObject, existentials: frozenset[ArbitraryObject]
    ) -> None:
        self.universal = universal
        self.existentials = existentials


def test_matroyshka(deps: frozenset[Dependency]):
    existentials: list[frozenset[ArbitraryObject]] = [d.existentials for d in deps]
    stack = existentials.copy()
    while stack:
        set1 = stack.pop(0)
        for set2 in stack:
            if not set1.issubset(set2) or set2.issubset(set1):
                raise ValueError(
                    f"Existential sets do not meet Matroyshka condition. \nSet1: {set1}\nSet2: {set2}"
                )


UniArbObjects = set[ArbitraryObject]
ExiArbObjects = set[ArbitraryObject]


def separate_arb_objects(
    arb_objects: set[ArbitraryObject],
) -> tuple[UniArbObjects, ExiArbObjects]:
    uni_objs = set()
    exi_objs = set()
    for obj in arb_objects:
        if obj.is_existential:
            exi_objs.add(obj)
        else:
            uni_objs.add(obj)
    return uni_objs, exi_objs


class DependencyRelation:
    dependencies: frozenset[Dependency]

    def __init__(self, dependencies: frozenset[Dependency]) -> None:
        test_matroyshka(dependencies)
        self.dependencies = dependencies

    def validate(self, states: stateset):
        uni_arb_objects, exi_arb_objects = separate_arb_objects(states.arb_objects)
        # universal to existentials that depend on them ( share a pair )
        for d in self.dependencies:
            if not d.existentials.issubset(exi_arb_objects):
                raise ValueError(
                    f"{d.existentials} not found in existential states {exi_arb_objects}"
                )
            if d.universal not in uni_arb_objects:
                raise ValueError(
                    f"{d.universal } not found in universal states {uni_arb_objects}"
                )


class View:
    stage: stateset
    supposition: stateset
    dependency_relation: DependencyRelation

    def __init__(
        self,
        stage: stateset,
        supposition: stateset,
        dependency_relation: DependencyRelation,
    ) -> None:
        self.stage = stage
        self.supposition = supposition
        dependency_relation.validate(stage.union(supposition))
        self.dependency_relation = dependency_relation
        total_emphasis = stage.has_emphasis + supposition.has_emphasis
        if total_emphasis == 2:
            raise ValueError("Both stage and supposition have an Emphasis")
        elif total_emphasis == 0:
            raise ValueError("Neither stage nor supposition has an Emphasis")
        # view has exactly one emphasis

    def __repr__(self) -> str:
        return f"<View \n  stage={pformat(self.stage)} \n  supposition={pformat(self.supposition)} \n  dep_rel={self.dependency_relation}\n>"


smokes = Predicate("smokes", 1)
existential_arb_set = ArbitraryObjectMaker(is_existential=True)
universal_arb_set = ArbitraryObjectMaker(is_existential=False)
john_smokes = Atom(smokes, (Term(f=Function("john", 0)),))
existent_arb_obj = next(existential_arb_set)
universal_arb = next(universal_arb_set)
arbitrary_object1_smokes = Atom(smokes, (universal_arb,))
arbitrary_object2_smokes = Atom(smokes, (Emphasis(existent_arb_obj),))

stage = stateset({john_smokes, arbitrary_object1_smokes, arbitrary_object2_smokes})
supposition = stateset(
    {john_smokes, arbitrary_object1_smokes, arbitrary_object1_smokes}
)
dep_relation = DependencyRelation(
    frozenset({Dependency(universal_arb, frozenset({existent_arb_obj}))})
)

v = View(stage, supposition, dep_relation)
print(v)
