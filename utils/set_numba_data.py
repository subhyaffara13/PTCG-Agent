
def set_numba_data(index: Index):
    numba_data = index._data
    if numba_data.dtype in (object, "string"):
        numba_data = np.asarray(numba_data)
        if not lib.is_string_array(numba_data):
            raise ValueError(
                "The numba engine only supports using string or numeric column names"
            )
        numba_data = numba_data.astype("U")
    try:
        index._numba_data = numba_data
        yield index
    finally:
        del index._numba_data

