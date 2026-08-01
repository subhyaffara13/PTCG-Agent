
def get_is_dtype_funcs():
    """
    Get all functions in pandas.core.dtypes.common that
    begin with 'is_' and end with 'dtype'

    """
    fnames = [f for f in dir(com) if (f.startswith("is_") and f.endswith("dtype"))]
    fnames.remove("is_string_or_object_np_dtype")  # fastpath requires np.dtype obj
    return [getattr(com, fname) for fname in fnames]

