
def _asfarray(x):
    """
    Convert to array with floating or complex dtype.

    float16 values are also promoted to float32.
    """
    if not hasattr(x, "dtype"):
        x = np.asarray(x)

    if x.dtype == np.float16:
        return np.asarray(x, np.float32)
    elif x.dtype.kind not in 'fc':
        return np.asarray(x, np.float64)

    # Require native byte order
    dtype = x.dtype.newbyteorder('=')
    # Always align input
    copy = True if not x.flags['ALIGNED'] else copy_if_needed
    return np.array(x, dtype=dtype, copy=copy)

