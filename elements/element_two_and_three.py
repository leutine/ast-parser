# coding: utf-8

from .element_main import ElementMain
from .element_one import ElementOne

from ..utils import get_element


@parse
class ElementTwo(ElementMain, ElementOne):
    """
    Element Two
    Short abbreviation: [two].
    """
    def __init__(self, name, timeout=20000):
        super().__init__(name, timeout)

    @get_element
    def input(self, value=None, length=10):
        print(f"Input value '{value}' if it is not None, else random value with length {length}")

    @get_element
    def clear(self):
        print(f"Clear element {self.name}")

    @get_element
    def update(self, value):
        print(f"Update element {self.name} with value {value} and {a}")


class ElementThree(ElementMain):
    def __init__(self, name, timeout):
        super().__init__(name, timeout)
