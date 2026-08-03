import os

def hb_read(path_or_open_file, *, spmatrix=_NoValue):
    """Read HB-format file.

    Parameters
    ----------
    path_or_open_file : path-like or file-like
        If a file-like object, it is used as-is. Otherwise, it is opened
        before reading.
    spmatrix : bool, optional (default: True)
        If ``True``, return sparse matrix. Otherwise return sparse array.

        .. deprecated:: 1.18.0
            The default value for `spmatrix` is changing to False in v1.20.
            That means the default return value will be a sparse array.
            Unless you use * instead of @, ** for matrix power, or you depend
            on 2D shapes from e.g. ``A.sum(axis=0)``, it may not matter to you.
            See :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.

    Returns
    -------
    data : csc_array or csc_matrix
        The data read from the HB file as a sparse array.

    Notes
    -----
    At the moment not the full Harwell-Boeing format is supported. Supported
    features are:

    - assembled, non-symmetric, real matrices
    - integer for pointer/indices
    - exponential format for float values, and int format

    Examples
    --------
    We can read and write a harwell-boeing format file:

    >>> from scipy.io import hb_read, hb_write
    >>> from scipy.sparse import csr_array, eye
    >>> data = csr_array(eye(3))  # create a sparse array
    >>> hb_write("data.hb", data)  # write a hb file
    >>> print(hb_read("data.hb", spmatrix=False))  # read a hb file
    <Compressed Sparse Column sparse array of dtype 'float64'
        with 3 stored elements and shape (3, 3)>
        Coords	Values
        (0, 0)	1.0
        (1, 1)	1.0
        (2, 2)	1.0
    """
    def _get_matrix(fid):
        hb = HBFile(fid)
        return hb.read_matrix()

    if hasattr(path_or_open_file, 'read'):
        data = _get_matrix(path_or_open_file)
    else:
        with open(path_or_open_file) as f:
            data = _get_matrix(f)

    if spmatrix is _NoValue:
        msg = """The default value for `spmatrix` is changing to `False` in v1.20.
            That means the default return type will be a sparse array.
            Unless you use * instead of @, ** for matrix power, or you depend
            on 2D shapes from e.g. `A.sum(axis=0)` it may not matter to you.
            See the spmatrix to sparray migration guide for details.
            https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html
            """
        prefixes = (os.path.dirname(__file__),)
        warnings.warn(msg, DeprecationWarning, skip_file_prefixes=prefixes)
        spmatrix = True

    if spmatrix:
        return csc_matrix(data)
    return data

