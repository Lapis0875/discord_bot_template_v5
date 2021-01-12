import inspect
import functools
from .type_hints import T


class ModulePrivateError(Exception):
    def __init__(self, o, *args, **kwargs):
        super().__init__(*args)
        self._msg: str = 'Object {} is a module-private method.'.format(
            o.__name__
        )

    @property
    def msg(self) -> str:
        return self._msg


def modulePrivate(o: T) -> T:
    # print('module-private decorator on object:', o)
    setattr(o, '__private__', True)
    if inspect.isfunction(o):
        @functools.wraps(o)
        def wrapper(*args, **kwargs):
            outerFrame: inspect.FrameInfo = inspect.getouterframes(inspect.currentframe())[1]
            originalFile: str = inspect.getfile(o)
            if outerFrame.filename == originalFile:
                # print('[Caller frame info]')
                # print('filename =', outerFrame.filename)
                # print('line number =', outerFrame.lineno)
                # print('function =', outerFrame.function)
                # print('code context =', outerFrame.code_context)
                # print('Same module. Allow using object.')
                return o(*args, **kwargs)
            else:
                # print('Different module. Deny using object.')
                raise ModulePrivateError(o)
        return wrapper
    elif inspect.ismethod(o):
        @functools.wraps(o)
        def wrapper(*args, **kwargs):
            outerFrame: inspect.FrameInfo = inspect.getouterframes(inspect.currentframe())[1]
            originalFile: str = inspect.getfile(o)
            if outerFrame.filename == originalFile:
                # print('[Caller frame info]')
                # print('filename =', outerFrame.filename)
                # print('line number =', outerFrame.lineno)
                # print('function =', outerFrame.function)
                # print('code context =', outerFrame.code_context)
                # print('Same module. Allow using object.')
                # print('Same module. Allow using object.')
                return o(*args, **kwargs)
            else:
                # print('Different module. Deny using object.')
                raise ModulePrivateError(o)
        return wrapper
    elif inspect.isclass(o):
        # Override '__new__' method to hook class object call.
        # '__call__' defines class instance's callable feature, which is not suitable to hook class object call.
        @functools.wraps(o.__new__)
        def __new__(cls: type, *args, **kwargs):
            outerFrame: inspect.FrameInfo = inspect.getouterframes(inspect.currentframe())[1]
            originalFile: str = inspect.getfile(o)
            if outerFrame.filename == originalFile:
                # print('[Caller frame info]')
                # print('filename =', outerFrame.filename)
                # print('line number =', outerFrame.lineno)
                # print('function =', outerFrame.function)
                # print('code context =', outerFrame.code_context)
                # print('Same module. Allow using object.')
                # print('Same module. Allow using object.')
                return cls.__new__(*args, **kwargs)
            else:
                # print('Different module. Deny using object.')
                raise ModulePrivateError(o)

        setattr(o, '__new__', __new__)
        return o
    else:
        raise ValueError('Cannot make this object into module-private!')
