
def dict_to_numpy_array(d, mapping=None):
    """Convert a dictionary of dictionaries to a numpy array
    with optional mapping."""
    try:
        return _dict_to_numpy_array2(d, mapping)
    except (AttributeError, TypeError):
        # AttributeError is when no mapping was provided and v.keys() fails.
        # TypeError is when a mapping was provided and d[k1][k2] fails.
        return _dict_to_numpy_array1(d, mapping)

