
def prod_numpy(a, *args, **kwargs):
    """
    The function will call np.prod with type as np.int64 if the input type
    is int or uint64 if is uint. This is necessary because windows np.prod uses by default
    int32 while on linux it uses int64.
    This is for fixing integer overflow https://github.com/pytorch/pytorch/issues/77320

    Returns:
        np.prod of input
    """
    if "dtype" not in kwargs:
        if np.issubdtype(a.dtype, np.signedinteger):
            a = a.astype(np.int64)
        elif np.issubdtype(a.dtype, np.unsignedinteger):
            a = a.astype(np.uint64)

    fn = reference_reduction_numpy(np.prod)
    return fn(a, *args, **kwargs)

