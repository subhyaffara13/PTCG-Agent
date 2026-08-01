
def chainable(method: Callable[[_T, ...], None]) -> Callable[[_T, ...], _T]:
    """
    Wrap an instance method to always return self.


    >>> class Dingus:
    ...     @chainable
    ...     def set_attr(self, name, val):
    ...         setattr(self, name, val)
    >>> d = Dingus().set_attr('a', 'eh!')
    >>> d.a
    'eh!'
    >>> d2 = Dingus().set_attr('a', 'eh!').set_attr('b', 'bee!')
    >>> d2.a + d2.b
    'eh!bee!'

    Enforces that the return value is null.

    >>> class BorkedDingus:
    ...     @chainable
    ...     def set_attr(self, name, val):
    ...         setattr(self, name, val)
    ...         return len(name)
    >>> BorkedDingus().set_attr('a', 'eh!')
    Traceback (most recent call last):
    ...
    AssertionError
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        assert method(self, *args, **kwargs) is None
        return self

    return wrapper

