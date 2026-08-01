
def _add_to_array(x_in, i_fixed, x_fixed):
    """Adds fixed variables back to an array"""
    i_free = ~i_fixed
    if x_in.ndim == 2:
        i_free = i_free[:, None] @ i_free[None, :]
    x_out = np.zeros_like(i_free, dtype=x_in.dtype)
    x_out[~i_free] = x_fixed
    x_out[i_free] = x_in.ravel()
    return x_out

