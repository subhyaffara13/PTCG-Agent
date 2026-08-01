
def _reconstruct(subtype, shape, dtype):
    from numpy import ndarray
    return ndarray.__new__(subtype, shape, dtype)

