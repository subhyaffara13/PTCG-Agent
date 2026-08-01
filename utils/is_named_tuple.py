
def is_named_tuple(obj):
  return (
    isinstance(obj, tuple)
    and hasattr(obj, '_fields')
    and hasattr(obj, '_asdict')
    and hasattr(obj, '_replace')
  )


def is_named_tuple(obj: object) -> bool:
    """
    Check if the object is a named tuple.

    Parameters
    ----------
    obj : object
        The object that will be checked to determine
        whether it is a named tuple.

    Returns
    -------
    bool
        Whether `obj` is a named tuple.

    See Also
    --------
    api.types.is_dict_like: Check if the object is dict-like.
    api.types.is_hashable: Return True if hash(obj)
                                  will succeed, False otherwise.
    api.types.is_categorical_dtype : Check if the dtype is categorical.

    Examples
    --------
    >>> from collections import namedtuple
    >>> from pandas.api.types import is_named_tuple
    >>> Point = namedtuple("Point", ["x", "y"])
    >>> p = Point(1, 2)
    >>>
    >>> is_named_tuple(p)
    True
    >>> is_named_tuple((1, 2))
    False
    """
    return isinstance(obj, abc.Sequence) and hasattr(obj, "_fields")

