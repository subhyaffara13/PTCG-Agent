
def shares_memory(left, right) -> bool:
    """
    Pandas-compat for np.shares_memory.
    """
    if isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
        return np.shares_memory(left, right)
    elif isinstance(left, np.ndarray):
        # Call with reversed args to get to unpacking logic below.
        return shares_memory(right, left)

    if isinstance(left, RangeIndex):
        return False
    if isinstance(left, MultiIndex):
        return shares_memory(left._codes, right)
    if isinstance(left, (Index, Series)):
        if isinstance(right, (Index, Series)):
            return shares_memory(left._values, right._values)
        return shares_memory(left._values, right)

    if isinstance(left, NDArrayBackedExtensionArray):
        return shares_memory(left._ndarray, right)
    if isinstance(left, pd.core.arrays.SparseArray):
        return shares_memory(left.sp_values, right)
    if isinstance(left, pd.core.arrays.IntervalArray):
        return shares_memory(left._left, right) or shares_memory(left._right, right)

    if isinstance(left, ArrowExtensionArray):
        if isinstance(right, ArrowExtensionArray):
            # https://github.com/pandas-dev/pandas/pull/43930#discussion_r736862669
            left_pa_data = left._pa_array
            right_pa_data = right._pa_array
            left_buf1 = left_pa_data.chunk(0).buffers()[1]
            right_buf1 = right_pa_data.chunk(0).buffers()[1]
            return left_buf1.address == right_buf1.address
        else:
            # if we have one one ArrowExtensionArray and one other array, assume
            # they can only share memory if they share the same numpy buffer
            return np.shares_memory(left, right)

    if isinstance(left, BaseMaskedArray) and isinstance(right, BaseMaskedArray):
        # By convention, we'll say these share memory if they share *either*
        #  the _data or the _mask
        return np.shares_memory(left._data, right._data) or np.shares_memory(
            left._mask, right._mask
        )

    if isinstance(left, DataFrame) and len(left._mgr.blocks) == 1:
        arr = left._mgr.blocks[0].values
        return shares_memory(arr, right)

    raise NotImplementedError(type(left), type(right))


def shares_memory(a, b, /, max_work=-1):
    """
    shares_memory(a, b, /, max_work=-1)

    Determine if two arrays share memory.

    .. warning::

       This function can be exponentially slow for some inputs, unless
       `max_work` is set to zero or a positive integer.
       If in doubt, use `numpy.may_share_memory` instead.

    Parameters
    ----------
    a, b : ndarray
        Input arrays
    max_work : int, optional
        Effort to spend on solving the overlap problem (maximum number
        of candidate solutions to consider). The following special
        values are recognized:

        max_work=-1 (default)
            The problem is solved exactly. In this case, the function returns
            True only if there is an element shared between the arrays. Finding
            the exact solution may take extremely long in some cases.
        max_work=0
            Only the memory bounds of a and b are checked.
            This is equivalent to using ``may_share_memory()``.

    Raises
    ------
    numpy.exceptions.TooHardError
        Exceeded max_work.

    Returns
    -------
    out : bool

    See Also
    --------
    may_share_memory

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2, 3, 4])
    >>> np.shares_memory(x, np.array([5, 6, 7]))
    False
    >>> np.shares_memory(x[::2], x)
    True
    >>> np.shares_memory(x[::2], x[1::2])
    False

    Checking whether two arrays share memory is NP-complete, and
    runtime may increase exponentially in the number of
    dimensions. Hence, `max_work` should generally be set to a finite
    number, as it is possible to construct examples that take
    extremely long to run:

    >>> from numpy.lib.stride_tricks import as_strided
    >>> x = np.zeros([192163377], dtype=np.int8)
    >>> x1 = as_strided(
    ...     x, strides=(36674, 61119, 85569), shape=(1049, 1049, 1049))
    >>> x2 = as_strided(
    ...     x[64023025:], strides=(12223, 12224, 1), shape=(1049, 1049, 1))
    >>> np.shares_memory(x1, x2, max_work=1000)
    Traceback (most recent call last):
    ...
    numpy.exceptions.TooHardError: Exceeded max_work

    Running ``np.shares_memory(x1, x2)`` without `max_work` set takes
    around 1 minute for this case. It is possible to find problems
    that take still significantly longer.

    """
    return (a, b)

