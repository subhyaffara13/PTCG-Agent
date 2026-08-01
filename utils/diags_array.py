
def diags_array(diagonals, /, *, offsets=0, shape=None, format=None, dtype=_NoValue):
    """
    Construct a sparse array from diagonals.

    Parameters
    ----------
    diagonals : sequence of array_like
        Sequence of arrays containing the array diagonals,
        corresponding to `offsets`.
    offsets : sequence of int or an int, optional
        Diagonals to set (repeated offsets are not allowed):
          - k = 0  the main diagonal (default)
          - k > 0  the kth upper diagonal
          - k < 0  the kth lower diagonal
    shape : tuple of int, optional
        Shape of the result. If omitted, a square array large enough
        to contain the diagonals is returned.
    format : {"dia", "csr", "csc", "lil", ...}, optional
        Matrix format of the result. By default (format=None) an
        appropriate sparse array format is returned. This choice is
        subject to change.
    dtype : dtype, optional
        Data type of the array.  If `dtype` is None, the output
        data type is determined by the data type of the input diagonals.

        Up until SciPy 1.19, the default behavior will be to return an array
        with an inexact (floating point) data type.  In particular, integer
        input will be converted to double precision floating point.  This
        behavior is deprecated, and in SciPy 1.19, the default behavior
        will be changed to return an array with the same data type as the
        input diagonals.  To adopt this behavior before version 1.19, use
        ``dtype=None``.

    Returns
    -------
    new_array : dia_array
        `dia_array` holding the values in `diagonals` offset from the main diagonal
        as indicated in `offsets`.

    See Also
    --------
    dia_array : constructor for the sparse DIAgonal format.

    Notes
    -----
    Repeated diagonal offsets are disallowed.

    The result from ``diags_array`` is the sparse equivalent of::

        np.diag(diagonals[0], offsets[0])
        + ...
        + np.diag(diagonals[k], offsets[k])

    ``diags_array`` differs from `dia_array` in the way it handles off-diagonals.
    Specifically, `dia_array` assumes the data input includes padding
    (ignored values) at the start/end of the rows for positive/negative
    offset, while ``diags_array`` assumes the input data has no padding.
    Each value in the input `diagonals` is used.

    .. versionadded:: 1.11

    Examples
    --------
    >>> from scipy.sparse import diags_array
    >>> diagonals = [[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0], [1.0, 2.0]]
    >>> diags_array(diagonals, offsets=[0, -1, 2]).toarray()
    array([[1., 0., 1., 0.],
           [1., 2., 0., 2.],
           [0., 2., 3., 0.],
           [0., 0., 3., 4.]])

    Broadcasting of scalars is supported (but shape needs to be
    specified):

    >>> diags_array([1.0, -2.0, 1.0], offsets=[-1, 0, 1], shape=(4, 4)).toarray()
    array([[-2.,  1.,  0.,  0.],
           [ 1., -2.,  1.,  0.],
           [ 0.,  1., -2.,  1.],
           [ 0.,  0.,  1., -2.]])


    If only one diagonal is wanted (as in `numpy.diag`), the following
    works as well:

    >>> diags_array([1.0, 2.0, 3.0], offsets=1).toarray()
    array([[ 0.,  1.,  0.,  0.],
           [ 0.,  0.,  2.,  0.],
           [ 0.,  0.,  0.,  3.],
           [ 0.,  0.,  0.,  0.]])
    """
    # if offsets is not a sequence, assume that there's only one diagonal
    if isscalarlike(offsets):
        # now check that there's actually only one diagonal
        if len(diagonals) == 0 or isscalarlike(diagonals[0]):
            diagonals = [np.atleast_1d(diagonals)]
        else:
            raise ValueError("Different number of diagonals and offsets.")
    else:
        diagonals = list(map(np.atleast_1d, diagonals))

    offsets = np.atleast_1d(offsets)

    # Basic check
    if len(diagonals) != len(offsets):
        raise ValueError("Different number of diagonals and offsets.")

    # Determine shape, if omitted
    if shape is None:
        m = len(diagonals[0]) + abs(int(offsets[0]))
        shape = (m, m)

    # Determine data type, if omitted
    if dtype is None:
        dtype = np.result_type(*diagonals)
    elif dtype is _NoValue:
        # This is the old deprecated behavior that uses np.common_type().
        # After the deprecation period, this elif branch can be removed,
        # and the default for the `dtype` parameter changed back to `None`.
        dtype = np.dtype(np.common_type(*diagonals))
        future_dtype = np.result_type(*diagonals)
        if (dtype != future_dtype):
            warn(
                f"Input has data type {future_dtype}, but the output has been cast "
                f"to {dtype}.  In the future, the output data type will match the "
                "input. To avoid this warning, set the `dtype` parameter to `None` "
                "to have the output dtype match the input, or set it to the "
                "desired output data type.",
                FutureWarning,
                skip_file_prefixes=(os.path.dirname(__file__),)
            )

    # Construct data array
    m, n = shape

    M = max([min(m + offset, n - offset) + max(0, offset)
             for offset in offsets])
    M = max(0, M)
    data_arr = np.zeros((len(offsets), M), dtype=dtype)

    K = min(m, n)

    for j, diagonal in enumerate(diagonals):
        offset = offsets[j]
        k = max(0, offset)
        length = min(m + offset, n - offset, K)
        if length < 0:
            raise ValueError(f"Offset {offset} (index {j}) out of bounds")
        try:
            data_arr[j, k:k+length] = diagonal[...,:length]
        except ValueError as e:
            if len(diagonal) != length and len(diagonal) != 1:
                raise ValueError(
                    f"Diagonal length (index {j}: {len(diagonal)} at"
                    f" offset {offset}) does not agree with array size ({m}, {n})."
                ) from e
            raise

    return dia_array((data_arr, offsets), shape=(m, n)).asformat(format)

