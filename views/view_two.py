# coding: utf-8

from ..elements import ElementOne
from ..elements import ElementTwo


class ViewTwo:
    first = ElementOne('name4', 5000)
    second = ElementOne('name5', 5000)

    third = ElementTwo('name6', 5000)
    fourth = ElementTwo('name7', 5000)

    class SubView:
        fifth = ElementTwo('name8', 5000)
        sixth = ElementTwo('name9', 5000)

        class SecondLevelOfSubView:
            seventh = ElementOne('name10', 5000)

    class SecondSubView:
        eighth = ElementOne('name11', 5000)

        class SecondLevelOfSecondSubView:
            ninth = ElementTwo('name12', 5000)
            tenth = ElementTwo('name13', 5000)

        class ThirdLevelOfSecondSubView:
            eleventh = ElementOne('name14', 5000)

