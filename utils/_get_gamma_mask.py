
def _get_gamma_mask(shape, default_value, conditioned_value, where):
    out = np.full(shape, default_value)
    np.copyto(out, conditioned_value, where=where, casting="unsafe")
    return out

