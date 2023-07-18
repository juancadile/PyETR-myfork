from pyetr import (
    ArbitraryObjectGenerator,
    Atom,
    Dependency,
    DependencyRelation,
    Emphasis,
    Function,
    Predicate,
    Term,
    View,
    stateset,
)
from pyetr.view import Commitment

smokes = Predicate("smokes", 1)
existential_arb_set = ArbitraryObjectGenerator(is_existential=True)
universal_arb_set = ArbitraryObjectGenerator(is_existential=False)
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

v1 = View(stage, supposition, dep_relation)
v2 = View(stage, supposition, dep_relation)

c = Commitment(v1, v2)

print(v1)
