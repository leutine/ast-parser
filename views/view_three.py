# coding: utf-8

from ..elements import ElementOne
from ..elements import ElementTwo


class ViewThree:
    one_firstelement = ElementOne('name15', 5000)

    two_firstelement = ElementTwo('name16', 5000)
    two_secondelement = ElementTwo('name17', 5000)

    class SubView:
        two_secondelement = ElementTwo('name18', 5000)

        class SecondLevelOfSubView:
            one_firstelement = ElementOne('name19', 5000)
            one_secondelement = ElementOne('name20', 5000)

    class SecondSubView:
        one_firstelement = ElementOne('name21', 5000)

        class SecondLevelOfSecondSubView:
            two_firstelement = ElementTwo('name22', 5000)
            two_secondelement = ElementTwo('name23', 5000)

    class ThirdSubView:
        one_firstelement = ElementOne('name24', 5000)

        class SecondLevelOfThirdSubView:
            one_firstelement = ElementOne('name25', 5000)

            class ThirdLevelOfThirdSubView:
                one_firstelement = ElementOne('name26', 5000)

