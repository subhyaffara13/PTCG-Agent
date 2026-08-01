
def integer_repr(x):
    """Return the signed-magnitude interpretation of the binary representation
    of x."""
    import numpy as np

    if x.dtype == np.float16:
        return _integer_repr(x, np.int16, np.int16(-(2**15)))
    elif x.dtype == np.float32:
        return _integer_repr(x, np.int32, np.int32(-(2**31)))
    elif x.dtype == np.float64:
        return _integer_repr(x, np.int64, np.int64(-(2**63)))
    else:
        raise ValueError(f"Unsupported dtype {x.dtype}")


def integer_repr(x):
    """Return the signed-magnitude interpretation of the binary representation
    of x."""
    import numpy as np
    if x.dtype == np.float16:
        return _integer_repr(x, np.int16, np.int16(-2**15))
    elif x.dtype == np.float32:
        return _integer_repr(x, np.int32, np.int32(-2**31))
    elif x.dtype == np.float64:
        return _integer_repr(x, np.int64, np.int64(-2**63))
    else:
        raise ValueError(f'Unsupported dtype {x.dtype}')

