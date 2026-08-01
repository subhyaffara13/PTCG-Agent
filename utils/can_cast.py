
def can_cast(from_, to, casting="safe"):
    from_ = _extract_dtype(from_)
    to_ = _extract_dtype(to)

    return _dtypes_impl.can_cast_impl(from_.torch_dtype, to_.torch_dtype, casting)


def can_cast(from_: DType | Array, to: DType, /) -> bool:
    if not isinstance(from_, torch.dtype):
        from_ = from_.dtype
    return torch.can_cast(from_, to)


def can_cast(from_, to, casting="safe"):
    """
    can_cast(from_, to, casting='safe')

    Returns True if cast between data types can occur according to the
    casting rule.

    Parameters
    ----------
    from_ : dtype, dtype specifier, NumPy scalar, or array
        Data type, NumPy scalar, or array to cast from.
    to : dtype or dtype specifier
        Data type to cast to.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur.

        * 'no' means the data types should not be cast at all.
        * 'equiv' means only byte-order changes are allowed.
        * 'safe' means only casts which can preserve values are allowed.
        * 'same_kind' means only safe casts or casts within a kind,
          like float64 to float32, are allowed.
        * 'unsafe' means any data conversions may be done.

    Returns
    -------
    out : bool
        True if cast can occur according to the casting rule.

    Notes
    -----
    .. versionchanged:: 2.0
       This function does not support Python scalars anymore and does not
       apply any value-based logic for 0-D arrays and NumPy scalars.

    See also
    --------
    dtype, result_type

    Examples
    --------
    Basic examples

    >>> import numpy as np
    >>> np.can_cast(np.int32, np.int64)
    True
    >>> np.can_cast(np.float64, complex)
    True
    >>> np.can_cast(complex, float)
    False

    >>> np.can_cast('i8', 'f8')
    True
    >>> np.can_cast('i8', 'f4')
    False
    >>> np.can_cast('i4', 'S4')
    False

    """
    return (from_,)

