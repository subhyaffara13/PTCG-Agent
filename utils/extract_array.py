
def extract_array(
    obj: Series | Index, extract_numpy: bool = ..., extract_range: bool = ...
) -> ArrayLike: ...


def extract_array(
    obj: T, extract_numpy: bool = ..., extract_range: bool = ...
) -> T | ArrayLike: ...


def extract_array(
    obj: T, extract_numpy: bool = False, extract_range: bool = False
) -> T | ArrayLike:
    """
    Extract the ndarray or ExtensionArray from a Series or Index.

    For all other types, `obj` is just returned as is.

    Parameters
    ----------
    obj : object
        For Series / Index, the underlying ExtensionArray is unboxed.

    extract_numpy : bool, default False
        Whether to extract the ndarray from a NumpyExtensionArray.

    extract_range : bool, default False
        If we have a RangeIndex, return range._values if True
        (which is a materialized integer ndarray), otherwise return unchanged.

    Returns
    -------
    arr : object

    Examples
    --------
    >>> extract_array(pd.Series(["a", "b", "c"], dtype="category"))
    ['a', 'b', 'c']
    Categories (3, str): ['a', 'b', 'c']

    Other objects like lists, arrays, and DataFrames are just passed through.

    >>> extract_array([1, 2, 3])
    [1, 2, 3]

    For an ndarray-backed Series / Index the ndarray is returned.

    >>> extract_array(pd.Series([1, 2, 3]))
    array([1, 2, 3])

    To extract all the way down to the ndarray, pass ``extract_numpy=True``.

    >>> extract_array(pd.Series([1, 2, 3]), extract_numpy=True)
    array([1, 2, 3])
    """
    typ = getattr(obj, "_typ", None)
    if typ in _typs:
        # i.e. isinstance(obj, (ABCIndex, ABCSeries))
        if typ == "rangeindex":
            if extract_range:
                # error: "T" has no attribute "_values"
                return obj._values  # type: ignore[attr-defined]
            return obj

        # error: "T" has no attribute "_values"
        return obj._values  # type: ignore[attr-defined]

    elif extract_numpy and typ == "npy_extension":
        # i.e. isinstance(obj, ABCNumpyExtensionArray)
        # error: "T" has no attribute "to_numpy"
        return obj.to_numpy()  # type: ignore[attr-defined]

    return obj

