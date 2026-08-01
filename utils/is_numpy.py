
def is_numpy(obj: Any) -> bool:
    if np is None:
        return False
    return isinstance(obj, (np.ndarray, np.generic)) or id(obj) in _numpy_function_ids

