from typing import Callable, Any


class FlagValue:
    def __init__(self, func: Callable[[Any], bytes]) -> None:
        self.__func__ = func
        self.__name__ = func.__qualname__ or func.__name__
        self._value = func(None)    # Pass 'None' to fill 'self' parameter.

    def __get__(self) -> bytes:
        return self._value
