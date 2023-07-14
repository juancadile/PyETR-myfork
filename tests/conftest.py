import pytest

from pyetr import ArbitraryObject, Function
from pyetr.term import Term


@pytest.fixture
def func():
    return Function("func", 1)


@pytest.fixture
def exi_arb_obj():
    return ArbitraryObject("x1", is_existential=True)


@pytest.fixture
def uni_arb_obj():
    return ArbitraryObject("x1", is_existential=False)


@pytest.fixture
def term(func, exi_arb_obj):
    return Term(func, (exi_arb_obj,))
