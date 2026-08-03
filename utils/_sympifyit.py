from typing import Callable

def _sympifyit(arg, retval=None) -> Callable[[Callable[[T1, T2], T3]], Callable[[T1, T2], T3]]:
    """
    decorator to smartly _sympify function arguments

    Explanation
    ===========

    @_sympifyit('other', NotImplemented)
    def add(self, other):
        ...

    In add, other can be thought of as already being a SymPy object.

    If it is not, the code is likely to catch an exception, then other will
    be explicitly _sympified, and the whole code restarted.

    if _sympify(arg) fails, NotImplemented will be returned

    See also
    ========

    __sympifyit
    """
    def deco(func):
        return __sympifyit(func, arg, retval)

    return deco


def _sympifyit(arg, retval=None):
    # This version of _sympifyit sympifies MutableMatrix objects
    def deco(func):
        @wraps(func)
        def __sympifyit_wrapper(a, b):
            try:
                b = _sympify(b)
                return func(a, b)
            except SympifyError:
                return retval

        return __sympifyit_wrapper

    return deco

