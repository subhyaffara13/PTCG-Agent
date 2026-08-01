
def _get_vectorize_dtype(dtype):
    if dtype.char in "SU":
        return dtype.char
    return dtype

