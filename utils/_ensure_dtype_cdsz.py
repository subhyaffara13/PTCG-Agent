
def _ensure_dtype_cdsz(*arrays):
    # Ensure that the dtype of arrays is one of the standard types
    # compatible with LAPACK functions (single or double precision
    # real or complex).
    dtype = np.result_type(*arrays)
    if not np.issubdtype(dtype, np.inexact):
        return (array.astype(np.float64) for array in arrays)
    complex = np.issubdtype(dtype, np.complexfloating)
    if np.finfo(dtype).bits <= 32:
        dtype = np.complex64 if complex else np.float32
    elif np.finfo(dtype).bits >= 64:
        dtype = np.complex128 if complex else np.float64
    return (array.astype(dtype, copy=False) for array in arrays)

