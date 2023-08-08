from pyetr.cases import BaseExample
from pyetr.inference import default_inference_procedure
from pyetr.parsing import parse_string_to_view as ps
from pyetr.view import View


class e1(BaseExample):
    """
    P1: Every archaeon has a nucleus; ∀x (IsArcheon(x) → HasNucleus(x))
    P2: Halobacterium is an archeon; IsArcheon(Halobacterium())

    C: Halobacterium is an archaeon and has a nucleus; IsArcheon(Halobacterium()) ∧ HasNucleus(Halobacterium())
    """

    v: tuple[View, View] = (
        ps("∀x (IsArcheon(x) → HasNucleus(x))"),
        ps("IsArcheon(Halobacterium())"),
    )
    c: View = ps("IsArcheon(Halobacterium()) ∧ HasNucleus(Halobacterium())")

    @classmethod
    def test(cls):
        result = default_inference_procedure(cls.v)
        assert result.is_equivalent_under_arb_sub(cls.c)


class UniProduct(BaseExample):
    v = (ps("∀x ∃a (P(x*) ∧ E(x,a)) ∨ ~P(x)"), ps("P(j()*)"))
    c = ps("∃a (P(j()*) ∧ E(j(),a)) ∨ ~P(j())")

    @classmethod
    def test(cls):
        result = cls.v[0].universal_product(cls.v[1])
        assert result.is_equivalent_under_arb_sub(cls.c)
