
def passthrough(func: Callable[..., object]) -> Callable[[_T], _T]:
    """
    Wrap the function to always return the first parameter.

    >>> passthrough(print)('3')
    3
    '3'
    """

    @functools.wraps(func)
    def wrapper(first: _T, *args, **kwargs) -> _T:
        func(first, *args, **kwargs)
        return first

    return wrapper  # type: ignore[return-value]


def passthrough(func: Callable[..., object]) -> Callable[[_T], _T]:
    """
    Wrap the function to always return the first parameter.

    >>> passthrough(print)('3')
    3
    '3'
    """

    @functools.wraps(func)
    def wrapper(first: _T, *args, **kwargs) -> _T:
        func(first, *args, **kwargs)
        return first

    return wrapper  # type: ignore[return-value]


def passthrough(func: Callable[..., object]) -> Callable[[_T], _T]:
    """
    Wrap the function to always return the first parameter.

    >>> passthrough(print)('3')
    3
    '3'
    """

    @functools.wraps(func)
    def wrapper(first: _T, *args, **kwargs) -> _T:
        func(first, *args, **kwargs)
        return first

    return wrapper

