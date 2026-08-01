
def bmat(blocks, format=None, dtype=None):
    """
    Build a sparse array or matrix from sparse sub-blocks.

    Note: `block_array` is preferred over ``bmat``. They are the same function
    except that ``bmat`` returns a deprecated sparse matrix when none of the
    inputs are sparse arrays.

    .. warning::

        This function returns a sparse matrix when no inputs are sparse arrays.
        You are encouraged to use `block_array` to take advantage
        of the sparse array functionality.

    Parameters
    ----------
    blocks : array_like
        Grid of sparse matrices with compatible shapes.
        An entry of None implies an all-zero matrix.
    format : {'bsr', 'coo', 'csc', 'csr', 'dia', 'dok', 'lil'}, optional
        The sparse format of the result (e.g. "csr"). By default an
        appropriate sparse matrix format is returned.
        This choice is subject to change.
    dtype : dtype, optional
        The data-type of the output matrix. If not given, the dtype is
        determined from that of `blocks`.

    Returns
    -------
    bmat : sparse matrix or array
        If any block in blocks is a sparse array, return a sparse array.
        Otherwise return a sparse matrix.

        If you want a sparse array built from blocks that are not sparse
        arrays, use ``block_array()``.

    See Also
    --------
    block_array

    Examples
    --------
    >>> from scipy.sparse import coo_array, bmat
    >>> A = coo_array([[1, 2], [3, 4]])
    >>> B = coo_array([[5], [6]])
    >>> C = coo_array([[7]])
    >>> bmat([[A, B], [None, C]]).toarray()
    array([[1, 2, 5],
           [3, 4, 6],
           [0, 0, 7]])

    >>> bmat([[A, None], [None, C]]).toarray()
    array([[1, 2, 0],
           [3, 4, 0],
           [0, 0, 7]])

    """
    blocks = np.asarray(blocks, dtype='object')
    if any(isinstance(b, sparray) for b in blocks.flat):
        return _block(blocks, format, dtype)
    else:
        return _block(blocks, format, dtype, return_spmatrix=True)


def bmat(obj, ldict=None, gdict=None):
    """
    Build a matrix object from a string, nested sequence, or array.

    Parameters
    ----------
    obj : str or array_like
        Input data. If a string, variables in the current scope may be
        referenced by name.
    ldict : dict, optional
        A dictionary that replaces local operands in current frame.
        Ignored if `obj` is not a string or `gdict` is None.
    gdict : dict, optional
        A dictionary that replaces global operands in current frame.
        Ignored if `obj` is not a string.

    Returns
    -------
    out : matrix
        Returns a matrix object, which is a specialized 2-D array.

    See Also
    --------
    block :
        A generalization of this function for N-d arrays, that returns normal
        ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.asmatrix('1 1; 1 1')
    >>> B = np.asmatrix('2 2; 2 2')
    >>> C = np.asmatrix('3 4; 5 6')
    >>> D = np.asmatrix('7 8; 9 0')

    All the following expressions construct the same block matrix:

    >>> np.bmat([[A, B], [C, D]])
    matrix([[1, 1, 2, 2],
            [1, 1, 2, 2],
            [3, 4, 7, 8],
            [5, 6, 9, 0]])
    >>> np.bmat(np.r_[np.c_[A, B], np.c_[C, D]])
    matrix([[1, 1, 2, 2],
            [1, 1, 2, 2],
            [3, 4, 7, 8],
            [5, 6, 9, 0]])
    >>> np.bmat('A,B; C,D')
    matrix([[1, 1, 2, 2],
            [1, 1, 2, 2],
            [3, 4, 7, 8],
            [5, 6, 9, 0]])

    """
    if isinstance(obj, str):
        if gdict is None:
            # get previous frame
            frame = sys._getframe().f_back
            glob_dict = frame.f_globals
            loc_dict = frame.f_locals
        else:
            glob_dict = gdict
            loc_dict = ldict

        return matrix(_from_string(obj, glob_dict, loc_dict))

    if isinstance(obj, (tuple, list)):
        # [[A,B],[C,D]]
        arr_rows = []
        for row in obj:
            if isinstance(row, N.ndarray):  # not 2-d
                return matrix(concatenate(obj, axis=-1))
            else:
                arr_rows.append(concatenate(row, axis=-1))
        return matrix(concatenate(arr_rows, axis=0))
    if isinstance(obj, N.ndarray):
        return matrix(obj)

