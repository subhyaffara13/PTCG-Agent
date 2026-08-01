
def _numpy_ref_transpose(a, dim0, dim1):
    if a.ndim <= 1:
        return a

    return np.swapaxes(a, dim0, dim1)

