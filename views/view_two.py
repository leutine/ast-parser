# coding: utf-8

from ..elements import ElementOne
from ..elements import ElementTwo


class ViewTwo:
    one_firstelement = ElementOne('name4', 5000)
    one_secondelement = ElementOne('name5', 5000)

    two_firstelement = ElementTwo('name6', 5000)
    two_secondelement = ElementTwo('name7', 5000)

    class SubView:
        two_firstelement = ElementTwo('name8', 5000)
        two_secondelement = ElementTwo('name9', 5000)

        class SecondLevelOfSubView:
            one_firstelement = ElementOne('name10', 5000)

    class SecondSubView:
        one_firstelement = ElementOne('name11', 5000)

        class SecondLevelOfSecondSubView:
            two_firstelement = ElementTwo('name12', 5000)
            two_secondelement = ElementTwo('name13', 5000)

        class ThirdLevelOfSecondSubView:
            one_firstelement = ElementOne('name14', 5000)

