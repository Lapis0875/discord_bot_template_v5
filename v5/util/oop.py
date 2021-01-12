"""
OOP Utility features

@Author Lapis0875
@Copyright 2020
"""
from typing import Final, ClassVar

__all__ = (
    'ClassPropertyMeta',
    'classproperty'
)

"""
[ Descriptors ]
'Descriptor' concept is an object's attribute which defines 'get', 'set', and 'del'.
Descriptors replaces old getter&setter expressions to modern ways.

In C#,
```cs
class DescriptorExample {
    String objectName {
        get { return "James" }
    }
}
```

Python has built-in descriptor class 'property' and you can use it as decorator on class's instance methods.
But, as it is only suitable for instance methods, I need to create my own descriptors for other situations.
"""


# Classmethod descriptor
class ClassPropertyMeta(type):
    """
    Metaclass for classes using classproperty
    """
    def __setattr__(self, key, value):
        obj = self.__dict__.get(key, None)
        if type(obj) is classproperty:
            return obj.__set__(self, value)
        return super().__setattr__(key, value)


class classproperty(object):
    """
    Similar to @property but used on classes instead of instances.
    The only caveat being that your class must use the
    classproperty.meta metaclass.
    Class properties will still work on class instances unless the
    class instance has overidden the class default. This is no different
    than how class instances normally work.
    Derived from: https://stackoverflow.com/a/5191224/721519
    class Z(object, metaclass=classproperty.meta):
        @classproperty
        def foo(cls):
            return 123
        _bar = None
        @classproperty
        def bar(cls):
            return cls._bar
        @bar.setter
        def bar(cls, value):
            return cls_bar = value
    Z.foo  # 123
    Z.bar  # None
    Z.bar = 222
    Z.bar  # 222
    """

    meta: Final[type] = ClassPropertyMeta

    def __init__(self, fget, fset=None):
        self.fget = self._fix_function(fget)
        self.fset = None if fset is None else self._fix_function(fset)

    def __get__(self, instance, owner=None):
        if not issubclass(type(owner), ClassPropertyMeta):
            raise TypeError(
                f"Class {owner} does not extend from the required "
                f"ClassPropertyMeta metaclass"
            )
        return self.fget.__get__(None, owner)()

    def __set__(self, owner, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        if not isinstance(owner, ClassPropertyMeta):
            owner = type(owner)
        return self.fset.__get__(None, owner)(value)

    def setter(self, fset):
        self.fset = self._fix_function(fset)
        return self

    _fn_types = (type(__init__), classmethod, staticmethod)

    @classmethod
    def _fix_function(cls, fn):
        if not isinstance(fn, cls._fn_types):
            raise TypeError("Getter or setter must be a function")
        # Always wrap in classmethod so we can call its __get__ and not
        # have to deal with difference between raw functions.
        if not isinstance(fn, (classmethod, staticmethod)):
            return classmethod(fn)
        return fn
