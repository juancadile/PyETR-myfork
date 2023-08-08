import pytest

from pyetr import Function
from pyetr.term import ArbitraryObject, Emphasis, Term


class TestFunction:
    def test_invalid_arity(self):
        with pytest.raises(ValueError, match="arity must not be less than 0"):
            Function("bad_func", -1)

    def test_valid(self):
        test = Function("good_func", 1)
        assert test.detailed == "Function(good_func, 1)"


class TestArbitraryObject:
    def test_valid_exi(self):
        test = ArbitraryObject("x1", is_existential=True)
        assert test.detailed == "<ArbitraryObject (Exi) name=x1>"

    def test_valid_uni(self):
        test = ArbitraryObject("x1", is_existential=False)
        assert test.detailed == "<ArbitraryObject (Uni) name=x1>"


class TestEmphasis:
    def test_valid_term(self, term):
        test = Emphasis(term)
        assert (
            test.detailed
            == "<Emphasis term=<Term f=Function(func, 1) t=(<ArbitraryObject (Exi) name=x1>,)>>"
        )

    def test_valid_arb_obj(self, exi_arb_obj):
        test = Emphasis(exi_arb_obj)
        assert test.detailed == "<Emphasis term=<ArbitraryObject (Exi) name=x1>>"

    def test_extract_arb_obj(self, exi_arb_obj):
        test = Emphasis(exi_arb_obj)
        assert exi_arb_obj in test.arb_objects


class TestTerm:
    def test_valid(self, func, exi_arb_obj):
        t = Term(func, (exi_arb_obj,))
        assert (
            t.detailed
            == "<Term f=Function(func, 1) t=(<ArbitraryObject (Exi) name=x1>,)>"
        )
