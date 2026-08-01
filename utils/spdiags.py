
def spdiags(data, diags, m=None, n=None, format=None):
    """
    Return a sparse matrix from diagonals.

    .. warning::

        This function returns a sparse matrix -- not a sparse array.
        You are encouraged to use `dia_array` to take advantage
        of the sparse array functionality. (See Notes below.)

    Parameters
    ----------
    data : array_like
        Matrix diagonals stored row-wise
    diags : sequence of int or an int
        Diagonals to set:

        * k = 0  the main diagonal
        * k > 0  the kth upper diagonal
        * k < 0  the kth lower diagonal
    m, n : int, tuple, optional
        Shape of the result. If `n` is None and `m` is a given tuple,
        the shape is this tuple. If omitted, the matrix is square and
        its shape is ``len(data[0])``.
    format : str, optional
        Format of the result. By default (format=None) an appropriate sparse
        matrix format is returned. This choice is subject to change.

    Returns
    -------
    new_matrix : sparse matrix
        `dia_matrix` format with values in ``data`` on diagonals from ``diags``.

    See Also
    --------
    diags_array : more convenient form of this function.
    diags : matrix version of diags_array.
    dia_matrix : the sparse DIAgonal format.

    Notes
    -----
    This function can be replaced by an equivalent call to `dia_matrix` as::

        dia_matrix((data, diags), shape=(m, n)).asformat(format)

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import spdiags
    >>> data = np.array([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    >>> diags = np.array([0, -1, 2])
    >>> spdiags(data, diags, 4, 4).toarray()
    array([[1, 0, 3, 0],
           [1, 2, 0, 4],
           [0, 2, 3, 0],
           [0, 0, 3, 4]])
    """
    if m is None and n is None:
        m = n = len(data[0])
    elif n is None:
        m, n = m
    return dia_matrix((data, diags), shape=(m, n)).asformat(format)

