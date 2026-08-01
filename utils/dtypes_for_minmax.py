
def dtypes_for_minmax(request):
    """
    Fixture of dtypes with min and max values used for testing
    cummin and cummax
    """
    dtype = request.param

    np_type = dtype
    if dtype == "Int64":
        np_type = np.int64
    elif dtype == "Float64":
        np_type = np.float64

    min_val = (
        np.iinfo(np_type).min
        if np.dtype(np_type).kind == "i"
        else np.finfo(np_type).min
    )
    max_val = (
        np.iinfo(np_type).max
        if np.dtype(np_type).kind == "i"
        else np.finfo(np_type).max
    )

    return (dtype, min_val, max_val)

