
def is_dataclass(item: object) -> bool:
    """
    Checks if the object is a data-class instance

    Parameters
    ----------
    item : object

    Returns
    --------
    is_dataclass : bool
        True if the item is an instance of a data-class,
        will return false if you pass the data class itself

    Examples
    --------
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Point:
    ...     x: int
    ...     y: int

    >>> is_dataclass(Point)
    False
    >>> is_dataclass(Point(0, 2))
    True

    """
    try:
        import dataclasses

        return dataclasses.is_dataclass(item) and not isinstance(item, type)
    except ImportError:
        return False


def is_dataclass(cdef: ClassDef) -> bool:
    return any(is_dataclass_decorator(d) for d in cdef.decorators)

