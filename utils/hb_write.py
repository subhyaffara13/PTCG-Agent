
def hb_write(path_or_open_file, m, hb_info=None):
    """Write HB-format file.

    Parameters
    ----------
    path_or_open_file : path-like or file-like
        If a file-like object, it is used as-is. Otherwise, it is opened
        before writing.
    m : sparse array or matrix
        the sparse array to write
    hb_info : HBInfo
        contains the meta-data for write

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
    m = m.tocsc(copy=False)

    if hb_info is None:
        hb_info = HBInfo.from_data(m)

    def _set_matrix(fid):
        hb = HBFile(fid, hb_info)
        hb.write_matrix(m)

    if hasattr(path_or_open_file, 'write'):
        _set_matrix(path_or_open_file)
    else:
        with open(path_or_open_file, 'w') as f:
            _set_matrix(f)

