
def bypass_unless(check):
    """
    Decorate a function to return its parameter unless ``check``.

    >>> enabled = [object()]  # True

    >>> @bypass_unless(enabled)
    ... def double(x):
    ...     return x * 2
    >>> double(2)
    4
    >>> del enabled[:]  # False
    >>> double(2)
    2
    """
    return bypass_when(check, _op=operator.not_)

