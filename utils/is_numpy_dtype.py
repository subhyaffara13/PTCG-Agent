
def is_numpy_dtype(obj: Any) -> bool:
    if np is None:
        return False
    return isinstance(obj, np.dtype)

