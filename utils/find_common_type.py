
def find_common_type(types: list[np.dtype]) -> np.dtype: ...


def find_common_type(types: list[ExtensionDtype]) -> DtypeObj: ...


def find_common_type(types: list[DtypeObj]) -> DtypeObj: ...


def find_common_type(types):
    """
    Find a common data type among the given dtypes.

    Parameters
    ----------
    types : list of dtypes

    Returns
    -------
    pandas extension or numpy dtype

    See Also
    --------
    numpy.find_common_type

    """
    if not types:
        raise ValueError("no types given")

    first = types[0]

    # workaround for find_common_type([np.dtype('datetime64[ns]')] * 2)
    # => object
    if lib.dtypes_all_equal(list(types)):
        return first

    # get unique types (dict.fromkeys is used as order-preserving set())
    types = list(dict.fromkeys(types).keys())

    if any(isinstance(t, ExtensionDtype) for t in types):
        for t in types:
            if isinstance(t, ExtensionDtype):
                res = t._get_common_dtype(types)
                if res is not None:
                    return res
        return np.dtype("object")

    # take lowest unit
    if all(lib.is_np_dtype(t, "M") for t in types):
        return np.dtype(max(types))
    if all(lib.is_np_dtype(t, "m") for t in types):
        return np.dtype(max(types))

    # don't mix bool / int or float or complex
    # this is different from numpy, which casts bool with float/int as int
    has_bools = any(t.kind == "b" for t in types)
    if has_bools:
        for t in types:
            if t.kind in "iufc":
                return np.dtype("object")

    return np_find_common_type(*types)

