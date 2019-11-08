# coding: utf-8

from .element_main import ElementMain

from ..utils import get_element


class ElementFour(ElementMain):
    def __init__(self, name, timeout=20000):
        super().__init__(name, timeout)

    @get_element
    def input(self, value=None, length=10):
        print(f"Input value '{value}' if it is not None, else random value with length {length}")
