__all__ = ["View", "Commitment"]

from pprint import pformat

from .dependency import DependencyRelation
from .stateset import set_of_states


class View:
    stage: set_of_states
    supposition: set_of_states
    dependency_relation: DependencyRelation

    def __init__(
        self,
        stage: set_of_states,
        supposition: set_of_states,
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


class Commitment:
    view1: View
    view2: View

    def __init__(self, view1: View, view2: View) -> None:
        self.view1 = view1
        self.view2 = view2


# class Variable:
#     name:str
#     def __init__(self, name) -> None:
#         self.name = name

# class Operator(Enum):
#     or_ = '∨'
#     and_ = '∧'
#     not_ = '¬'
#     truth = 'T'
#     falsum = '⊥'

# expr = Variable('x')
# #∃x ∃y ∀z ∀w (King(x) ∧ Queen(y) ∧ (King(z) → z = x) ∧ (Queen(w) → w = y))
# Predicate()
# def build_view(formula) -> View:

# #∀x [S(x) → (D(x) ∨ Sm(x))]

# translate sentence into the language of predicate calculus

# example 47 to 58
