# coding: utf-8

from .element_main import ElementMain
from ..utils.decorators import get_element


@parse
class ElementOne(ElementMain):
    """
    Element One
    Short abbreviation: [one].
    """
    def __init__(self, name, timeout=20000):
        super().__init__(name, timeout)

    def special_method(self, param):
        print(self.name, param)
