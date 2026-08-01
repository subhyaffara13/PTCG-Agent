
def primitive_column_to_ndarray(col: Column) -> tuple[np.ndarray, Any]:
    """
    Convert a column holding one of the primitive dtypes to a NumPy array.

    A primitive type is one of: int, uint, float, bool.

    Parameters
    ----------
    col : Column

    Returns
    -------
    tuple
        Tuple of np.ndarray holding the data and the memory owner object
        that keeps the memory alive.
    """
    buffers = col.get_buffers()

    data_buff, data_dtype = buffers["data"]
    data = buffer_to_ndarray(
        data_buff, data_dtype, offset=col.offset, length=col.size()
    )

    data = set_nulls(data, col, buffers["validity"])
    return data, buffers

