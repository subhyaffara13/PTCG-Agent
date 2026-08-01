
def diags(diagonals, offsets=0, shape=None, format=None, dtype=_NoValue):
    """
    Construct a sparse matrix from diagonals.

    .. warning::

        This function returns a sparse matrix -- not a sparse array.
        You are encouraged to use `diags_array` to take advantage
        of the sparse array functionality.

    Parameters
    ----------
    diagonals : sequence of array_like
        Sequence of arrays containing the matrix diagonals,
        corresponding to `offsets`.
    offsets : sequence of int or an int, optional
        Diagonals to set (repeated offsets are not allowed):
          - k = 0  the main diagonal (default)
          - k > 0  the kth upper diagonal
          - k < 0  the kth lower diagonal
    shape : tuple of int, optional
        Shape of the result. If omitted, a square matrix large enough
        to contain the diagonals is returned.
    format : {"dia", "csr", "csc", "lil", ...}, optional
        Matrix format of the result. By default (format=None) an
        appropriate sparse matrix format is returned. This choice is
        subject to change.
    dtype : dtype, optional
        Data type of the matrix.  If `dtype` is None, the output
        data type is determined by the data type of the input diagonals.

        Up until SciPy 1.19, the default behavior will be to return a matrix
        with an inexact (floating point) data type.  In particular, integer
        input will be converted to double precision floating point.  This
        behavior is deprecated, and in SciPy 1.19, the default behavior
        will be changed to return a matrix with the same data type as the
        input diagonals.  To adopt this behavior before version 1.19, use
        `dtype=None`.

    Returns
    -------
    new_matrix : dia_matrix
        `dia_matrix` holding the values in `diagonals` offset from the main diagonal
        as indicated in `offsets`.

    See Also
    --------
    spdiags : construct matrix from diagonals
    diags_array : construct sparse array instead of sparse matrix

    Notes
    -----
    Repeated diagonal offsets are disallowed.

    The result from ``diags`` is the sparse equivalent of::

        np.diag(diagonals[0], offsets[0])
        + ...
        + np.diag(diagonals[k], offsets[k])

    ``diags`` differs from `dia_matrix` in the way it handles off-diagonals.
    Specifically, `dia_matrix` assumes the data input includes padding
    (ignored values) at the start/end of the rows for positive/negative
    offset, while ``diags`` assumes the input data has no padding.
    Each value in the input `diagonals` is used.

    .. versionadded:: 0.11

    Examples
    --------
    >>> from scipy.sparse import diags
    >>> diagonals = [[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0], [1.0, 2.0]]
    >>> diags(diagonals, [0, -1, 2]).toarray()
    array([[1., 0., 1., 0.],
           [1., 2., 0., 2.],
           [0., 2., 3., 0.],
           [0., 0., 3., 4.]])

    Broadcasting of scalars is supported (but shape needs to be
    specified):

    >>> diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(4, 4)).toarray()
    array([[-2.,  1.,  0.,  0.],
           [ 1., -2.,  1.,  0.],
           [ 0.,  1., -2.,  1.],
           [ 0.,  0.,  1., -2.]])


    If only one diagonal is wanted (as in `numpy.diag`), the following
    works as well:

    >>> diags([1.0, 2.0, 3.0], 1).toarray()
    array([[ 0.,  1.,  0.,  0.],
           [ 0.,  0.,  2.,  0.],
           [ 0.,  0.,  0.,  3.],
           [ 0.,  0.,  0.,  0.]])
    """
    A = diags_array(diagonals, offsets=offsets, shape=shape, dtype=dtype)
    return dia_matrix(A).asformat(format)

