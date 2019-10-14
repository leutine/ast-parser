# -*- coding: utf-8 -*-

from ..utils import get_element


@parse
class ElementMain:
    """
    Base element with common methods.
    """
    def __init__(self, name, timeout):
        self.name = name
        self.timeout = timeout

    def __repr__(self):
        """
        'Raw' representation of element.
        :return: Class' name and its parameters (str)
        """
        return f"{self.__class__.__name__}('{self.name}', {self.timeout})"

    def __str__(self):
        """
        String representation of element.
        :return: text information about element (str)
        """
        return f"{self.name}"

    def _get(self):
        """Get element and return object"""
        print("Getting element...")

    @get_element
    def _get_children(self):
        return "get_children"

    def _find_all_elements(self, element_type):
        return f"find_all_elements of type {element_type}"

    @get_element
    def click(self):
        print(f"Clicking of element {self.name}")
