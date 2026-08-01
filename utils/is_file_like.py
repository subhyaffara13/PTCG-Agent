
def is_file_like(obj: object) -> bool:
    """
    Check if the object is a file-like object.

    For objects to be considered file-like, they must
    be an iterator AND have either a `read` and/or `write`
    method as an attribute.

    Note: file-like objects must be iterable, but
    iterable objects need not be file-like.

    Parameters
    ----------
    obj : object
        The object to check for file-like properties.
        This can be any Python object, and the function will
        check if it has attributes typically associated with
        file-like objects (e.g., `read`, `write`, `__iter__`).

    Returns
    -------
    bool
        Whether `obj` has file-like properties.

    See Also
    --------
    api.types.is_dict_like : Check if the object is dict-like.
    api.types.is_hashable : Return True if hash(obj) will succeed, False otherwise.
    api.types.is_named_tuple : Check if the object is a named tuple.
    api.types.is_iterator : Check if the object is an iterator.

    Examples
    --------
    >>> import io
    >>> from pandas.api.types import is_file_like
    >>> buffer = io.StringIO("data")
    >>> is_file_like(buffer)
    True
    >>> is_file_like([1, 2, 3])
    False
    """
    if not (hasattr(obj, "read") or hasattr(obj, "write")):
        return False

    return bool(hasattr(obj, "__iter__"))

