
def validate_tol(rtol, atol, n):
    """Validate tolerance values."""

    if np.any(rtol < 100 * EPS):
        warn("At least one element of `rtol` is too small. "
             f"Setting `rtol = np.maximum(rtol, {100 * EPS})`.",
             stacklevel=3)
        rtol = np.maximum(rtol, 100 * EPS)

    atol = np.asarray(atol)
    if atol.ndim > 0 and atol.shape != (n,):
        raise ValueError("`atol` has wrong shape.")

    if np.any(atol < 0):
        raise ValueError("`atol` must be positive.")

    return rtol, atol

