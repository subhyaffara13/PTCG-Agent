
def dtype_is_implied(dtype):
    """
    Determine if the given dtype is implied by the representation
    of its values.

    Parameters
    ----------
    dtype : dtype
        Data type

    Returns
    -------
    implied : bool
        True if the dtype is implied by the representation of its values.

    Examples
    --------
    >>> import numpy as np
    >>> np._core.arrayprint.dtype_is_implied(int)
    True
    >>> np.array([1, 2, 3], int)
    array([1, 2, 3])
    >>> np._core.arrayprint.dtype_is_implied(np.int8)
    False
    >>> np.array([1, 2, 3], np.int8)
    array([1, 2, 3], dtype=int8)
    """
    dtype = np.dtype(dtype)
    if format_options.get()['legacy'] <= 113 and dtype.type == np.bool:
        return False

    # not just void types can be structured, and names are not part of the repr
    if dtype.names is not None:
        return False

    # should care about endianness *unless size is 1* (e.g., int8, bool)
    if not dtype.isnative:
        return False

    return dtype.type in _typelessdata

