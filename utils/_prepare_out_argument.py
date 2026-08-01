
def _prepare_out_argument(out, dtype, expected_shape):
    if out is None:
        return np.empty(expected_shape, dtype=dtype)

    if out.shape != expected_shape:
        raise ValueError("Output array has incorrect shape.")
    if not out.flags.c_contiguous:
        raise ValueError("Output array must be C-contiguous.")
    if out.dtype != np.float64:
        raise ValueError("Output array must be double type.")
    return out

