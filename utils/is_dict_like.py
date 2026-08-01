
def is_dict_like(obj: object) -> bool:
    """
    Check if the object is dict-like.

    Parameters
    ----------
    obj : object
        The object to check. This can be any Python object,
        and the function will determine whether it
        behaves like a dictionary.

    Returns
    -------
    bool
        Whether `obj` has dict-like properties.

    See Also
    --------
    api.types.is_list_like : Check if the object is list-like.
    api.types.is_file_like : Check if the object is a file-like.
    api.types.is_named_tuple : Check if the object is a named tuple.

    Examples
    --------
    >>> from pandas.api.types import is_dict_like
    >>> is_dict_like({1: 2})
    True
    >>> is_dict_like([1, 2, 3])
    False
    >>> is_dict_like(dict)
    False
    >>> is_dict_like(dict())
    True
    """
    dict_like_attrs = ("__getitem__", "keys", "__contains__")
    return (
        all(hasattr(obj, attr) for attr in dict_like_attrs)
        # [GH 25196] exclude classes
        and not isinstance(obj, type)
    )

