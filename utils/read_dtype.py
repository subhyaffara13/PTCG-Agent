
def read_dtype(mat_stream, a_dtype):
    """
    Generic get of byte stream data of known type

    Parameters
    ----------
    mat_stream : file_like object
        MATLAB (tm) mat file stream
    a_dtype : dtype
        dtype of array to read. `a_dtype` is assumed to be correct
        endianness.

    Returns
    -------
    arr : ndarray
        Array of dtype `a_dtype` read from stream.

    """
    num_bytes = a_dtype.itemsize
    arr = np.ndarray(shape=(),
                     dtype=a_dtype,
                     buffer=mat_stream.read(num_bytes),
                     order='F')
    return arr

