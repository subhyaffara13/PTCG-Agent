
def is_static(func: FuncBase | Decorator) -> bool:
    if isinstance(func, Decorator):
        return is_static(func.func)
    elif isinstance(func, FuncBase):
        return func.is_static
    assert False, f"Unexpected func type: {type(func)}"


def is_static(value: object) -> bool:
    """
    >>> is_static(a := Dict({'a': 1}))
    True
    >>> is_static(dict(a))
    False
    >>> is_static(b := List([1, 2, 3]))
    True
    >>> is_static(list(b))
    False
    """
    return isinstance(value, Static) and not value._mutated_

