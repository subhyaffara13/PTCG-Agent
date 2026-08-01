
def get_sum_dtype(dtype: np.dtype) -> np.dtype | type[np.generic]:
    """Mimic numpy's casting for np.sum"""
    if dtype.kind == 'u' and np.can_cast(dtype, np.uint):
        return np.uint
    if np.can_cast(dtype, np.int_):
        return np.int_
    return dtype

