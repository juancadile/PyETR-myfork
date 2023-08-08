from .stateset import SetOfStates, State
from .view import View


def basic_step(v: tuple[View, ...]) -> View:
    verum = SetOfStates({State({})})
    falsum = SetOfStates({})
    empty_dep = frozenset({})
    out = View.from_deps(verum, verum, empty_dep)
    for i, view in enumerate(v):
        if i == 0:
            out = out.update(view.depose())
        else:
            out = out.update(view)
    return out.factor(View.from_deps(falsum, verum, empty_dep))


def default_inference_procedure(v: tuple[View, ...]) -> View:
    g_prime = basic_step(v)
    for i, view in enumerate(v):
        if i == 0:
            g_prime = g_prime.factor(view.depose())
        else:
            g_prime = g_prime.factor(view)
    return g_prime
