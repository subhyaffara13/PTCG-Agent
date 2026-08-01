
def eye_array(m, n=None, *, k=0, dtype=float, format=None):
    """Sparse array of chosen shape with ones on the kth diagonal and zeros elsewhere.

    Return a sparse array with ones on diagonal.
    Specifically a sparse array (m x n) where the kth diagonal
    is all ones and everything else is zeros.

    Parameters
    ----------
    m : int
        Number of rows requested.
    n : int, optional
        Number of columns. Default: `m`.
    k : int, optional
        Diagonal to place ones on. Default: 0 (main diagonal).
    dtype : dtype, optional
        Data type of the array
    format : str, optional (default: "dia")
        Sparse format of the result, e.g., format="csr", etc.

    Returns
    -------
    new_array : sparse array
        Sparse array of chosen shape with ones on the kth diagonal and zeros elsewhere.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy as sp
    >>> sp.sparse.eye_array(3).toarray()
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    >>> sp.sparse.eye_array(3, dtype=np.int8)
    <DIAgonal sparse array of dtype 'int8'
        with 3 stored elements (1 diagonals) and shape (3, 3)>

    """
    # TODO: delete next 15 lines [combine with _eye()] once spmatrix removed
    return _eye(m, n, k, dtype, format)

