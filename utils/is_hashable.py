
def is_hashable(x: VariableTracker) -> bool:
    # NB - performing isinstance check on a LazVT realizes the VT, accidentally
    # inserting the guard. To avoid this, lazyVT `is_hashable` methods looks at
    # the underlying value without realizing the VT. Consider updating the
    # lazyVT `is_hashable` method if you see unnecessary guarding for a key VT.
    if (
        isinstance(x, variables.LazyVariableTracker)
        and not x.is_realized()
        and x.is_hashable()
    ):
        return True
    return x.is_python_hashable()


def is_hashable(node: nodes.NodeNG) -> bool:
    """Return whether any inferred value of `node` is hashable.

    When finding ambiguity, return True.
    """
    # pylint: disable = too-many-try-statements
    try:
        for inferred in node.infer():
            if isinstance(inferred, (nodes.ClassDef, util.UninferableBase)):
                return True
            if not hasattr(inferred, "igetattr"):
                return True
            hash_fn = next(inferred.igetattr("__hash__"))
            if hash_fn.parent is inferred:
                return True
            if getattr(hash_fn, "value", True) is not None:
                return True
        return False
    except astroid.InferenceError:
        return True


def is_hashable(tp: Any, /) -> bool:
    """Return whether the provided argument is the `Hashable` class.

    ```python {test="skip" lint="skip"}
    is_hashable(Hashable)
    #> True
    ```
    """
    # `get_origin` is documented as normalizing any typing-module aliases to `collections` classes,
    # hence the second check:
    return tp is collections.abc.Hashable or get_origin(tp) is collections.abc.Hashable


def is_hashable(obj: object, allow_slice: bool = True) -> TypeGuard[Hashable]:
    """
    Return True if hash(obj) will succeed, False otherwise.

    Some types will pass a test against collections.abc.Hashable but fail when
    they are actually hashed with hash().

    Distinguish between these and other types by trying the call to hash() and
    seeing if they raise TypeError.

    Parameters
    ----------
    obj : object
        The object to check for hashability. Any Python object can be passed here.
    allow_slice : bool
        If True, return True if the object is hashable (including slices).
        If False, return True if the object is hashable and not a slice.

    Returns
    -------
    bool
        True if object can be hashed (i.e., does not raise TypeError when
        passed to hash()) and passes the slice check according to 'allow_slice'.
        False otherwise (e.g., if object is mutable like a list or dictionary
        or if allow_slice is False and object is a slice or contains a slice).

    See Also
    --------
    api.types.is_float : Return True if given object is float.
    api.types.is_iterator : Check if the object is an iterator.
    api.types.is_list_like : Check if the object is list-like.
    api.types.is_dict_like : Check if the object is dict-like.

    Examples
    --------
    >>> import collections
    >>> from pandas.api.types import is_hashable
    >>> a = ([],)
    >>> isinstance(a, collections.abc.Hashable)
    True
    >>> is_hashable(a)
    False
    """
    # Unfortunately, we can't use isinstance(obj, collections.abc.Hashable),
    # which can be faster than calling hash. That is because numpy scalars
    # fail this test.

    # Reconsider this decision once this numpy bug is fixed:
    # https://github.com/numpy/numpy/issues/5562

    if allow_slice is False:
        if isinstance(obj, tuple) and any(isinstance(v, slice) for v in obj):
            return False
        elif isinstance(obj, slice):
            return False

    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True


def is_hashable(arg):
  try:
    hash(arg)
    return True
  except TypeError:
    return False

