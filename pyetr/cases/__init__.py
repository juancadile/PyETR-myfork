__all__ = ["BaseExample"]
from abc import ABCMeta, abstractmethod
from typing import cast

from pyetr.view import View


class BaseExample(metaclass=ABCMeta):
    v: tuple[View, ...]
    c: View

    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "v"):
            raise TypeError("Example must have attribute v")
        if not hasattr(cls, "c"):
            raise TypeError("Example must have attribute c")
        v = getattr(cls, "v")
        assert isinstance(v, tuple)
        for i in v:
            assert isinstance(i, View)
        v = cast(tuple[View, ...], v)
        c = getattr(cls, "c")
        assert isinstance(c, View)

    @classmethod
    @abstractmethod
    def test(cls):
        raise NotImplementedError
