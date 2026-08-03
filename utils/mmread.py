import os

def mmread(source, *, spmatrix=_NoValue):
    """
    Reads the contents of a Matrix Market file-like 'source' into a matrix.

    Parameters
    ----------
    source : str or file-like
        Matrix Market filename (extensions .mtx, .mtz.gz)
        or open file-like object.
    spmatrix : bool, optional (default: True)
        If ``True``, return sparse matrix. Otherwise return sparse array.

        .. deprecated:: 1.18.0
            The default value for `spmatrix` is changing to False in v1.20.
            That means the default return value will be a sparse array.
            Unless you use * instead of @, ** for matrix power, or you depend
            on 2D shapes from e.g. ``A.sum(axis=0)`` it may not matter to you.
            See :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.

    Returns
    -------
    a : ndarray or coo_array or coo_matrix
        Dense or sparse array depending on the matrix format in the
        Matrix Market file.

    Examples
    --------
    >>> from io import StringIO
    >>> from scipy.io import mmread

    >>> text = '''%%MatrixMarket matrix coordinate real general
    ...  5 5 7
    ...  2 3 1.0
    ...  3 4 2.0
    ...  3 5 3.0
    ...  4 1 4.0
    ...  4 2 5.0
    ...  4 3 6.0
    ...  4 4 7.0
    ... '''

    ``mmread(source)`` returns the data as sparse matrix in COO format.

    >>> m = mmread(StringIO(text), spmatrix=False)
    >>> m
    <COOrdinate sparse array of dtype 'float64'
         with 7 stored elements and shape (5, 5)>
    >>> m.toarray()
    array([[0., 0., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 2., 3.],
           [4., 5., 6., 7., 0.],
           [0., 0., 0., 0., 0.]])
    """
    return MMFile().read(source, spmatrix=spmatrix)


def mmread(source, *, spmatrix=_NoValue):
    """
    Reads the contents of a Matrix Market file-like 'source' into a matrix.

    Parameters
    ----------
    source : str or file-like
        Matrix Market filename (extensions .mtx, .mtz.gz)
        or open file-like object.
    spmatrix : bool, optional (default: True)
        If ``True``, return sparse matrix. Otherwise return sparse array.

        .. deprecated:: 1.18.0
            The default value for `spmatrix` is changing to False in v1.20.
            That means the default return value will be a sparse array.
            Unless you use * instead of @, ** for matrix power, or you depend
            on 2D shapes from e.g. ``A.sum(axis=0)`` it may not matter to you.
            See :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.

    Returns
    -------
    a : ndarray or coo_array
        Dense or sparse array depending on the matrix format in the
        Matrix Market file.

    Notes
    -----
    .. versionchanged:: 1.12.0
        C++ implementation.

    Examples
    --------
    >>> from io import StringIO
    >>> from scipy.io import mmread

    >>> text = '''%%MatrixMarket matrix coordinate real general
    ...  5 5 7
    ...  2 3 1.0
    ...  3 4 2.0
    ...  3 5 3.0
    ...  4 1 4.0
    ...  4 2 5.0
    ...  4 3 6.0
    ...  4 4 7.0
    ... '''

    ``mmread(source)`` returns the data as sparse array in COO format.

    >>> m = mmread(StringIO(text), spmatrix=False)
    >>> m
    <COOrdinate sparse array of dtype 'float64'
        with 7 stored elements and shape (5, 5)>
    >>> m.toarray()
    array([[0., 0., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 2., 3.],
           [4., 5., 6., 7., 0.],
           [0., 0., 0., 0., 0.]])

    This method is threaded.
    The default number of threads is equal to the number of CPUs in the system.
    Use `threadpoolctl <https://github.com/joblib/threadpoolctl>`_ to override:

    >>> import threadpoolctl
    >>>
    >>> with threadpoolctl.threadpool_limits(limits=2):
    ...     m = mmread(StringIO(text), spmatrix=False)

    """
    cursor, stream_to_close = _get_read_cursor(source)

    if cursor.header.format == "array":
        mat = _read_body_array(cursor)
        if stream_to_close:
            stream_to_close.close()
        return mat
    else:
        triplet, shape = _read_body_coo(cursor, generalize_symmetry=True)
        if stream_to_close:
            stream_to_close.close()

        if spmatrix is _NoValue:
            msg = """The default value for `spmatrix` is changing to `False` in v1.20.
             That means the default return type will be a sparse array.
             Unless you use * instead of @, ** for matrix power, or you depend
             on 2D shapes from e.g. `A.sum(axis=0)` it may not matter to you.
             See the spmatrix to sparray migration guide for details.
             https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html
             """
            prefixes = (os.path.dirname(__file__),)
            warn(msg, DeprecationWarning, skip_file_prefixes=prefixes)
            spmatrix = True

        if spmatrix:
            return coo_matrix(triplet, shape=shape)
        return coo_array(triplet, shape=shape)

