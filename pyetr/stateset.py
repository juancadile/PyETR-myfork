__all__ = ["stateset"]
from typing import AbstractSet, Iterable, Optional

from .atom import Atom
from .term import ArbitraryObject


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
