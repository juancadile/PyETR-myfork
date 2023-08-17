import pytest

from pyetr import parse_string_to_view
from pyetr.parsing import parse_view_to_string


class TestFunction:
    def test_parse(self):
        input_string = "(Jack(Card()) ∨ Ace(Card()))"
        output_string = parse_view_to_string(parse_string_to_view(input_string))
        alt_string = "(Ace(Card()) ∨ Jack(Card()))"
        assert output_string == input_string or output_string == alt_string
