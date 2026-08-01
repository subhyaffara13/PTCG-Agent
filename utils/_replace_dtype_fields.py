
def _replace_dtype_fields(dtype, primitive_dtype):
    """
    Construct a dtype description list from a given dtype.

    Returns a new dtype object, with all fields and subtypes in the given type
    recursively replaced with `primitive_dtype`.

    Arguments are coerced to dtypes first.
    """
    dtype = np.dtype(dtype)
    primitive_dtype = np.dtype(primitive_dtype)
    return _replace_dtype_fields_recursive(dtype, primitive_dtype)

