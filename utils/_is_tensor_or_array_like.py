
def _is_tensor_or_array_like(value):
    """
    Check if a value is array-like (includes ragged arrays)
    """
    if is_numpy_array(value):
        return True
    if is_torch_tensor(value):
        return True
    if isinstance(value, (int, float, bool, np.number)):
        return True

    if isinstance(value, (list, tuple)):
        if len(value) == 0:
            # consider empty list or nested list as array-like
            return True
        return _is_tensor_or_array_like(value[0])

    return False

