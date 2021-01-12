"""
Design pattern implementations in python.

@Author Lapis0875
@Copyright 2020
"""
from typing import Dict


class SingletonMeta(type):
    """
    Metaclass which makes a class into singleton class.
    """
    __instances__: Dict[type, object] = {}

    def __call__(cls, *args, **kwargs):
        try:
            return  cls.__instances__[cls]
        except KeyError:
            cls.__instances__[cls] = super().__call__(*args, **kwargs)
            return cls.__instances__[cls]
