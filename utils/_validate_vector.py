
def _validate_vector(u, dtype=None):
    # XXX Is order='c' really necessary?
    u = np.asarray(u, dtype=dtype, order='c')
    if u.ndim == 1:
        return u
    raise ValueError("Input vector should be 1-D.")

