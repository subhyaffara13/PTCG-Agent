
def _real_roots_in_01(coeffs):
    """
    Find real roots of a polynomial in the interval [0, 1].

    For polynomials of degree <= 2, closed-form solutions are used.
    For higher degrees, `numpy.roots` is used as a fallback. In practice,
    matplotlib only ever uses cubic bezier curves and axis_aligned_extrema()
    differentiates, so we only ever find roots for degree <= 2.

    Parameters
    ----------
    coeffs : array-like
        Polynomial coefficients in ascending order:
        ``c[0] + c[1]*x + c[2]*x**2 + ...``
        Note this is the opposite convention from `numpy.roots`.

    Returns
    -------
    roots : ndarray
        Sorted array of real roots in [0, 1].
    """
    coeffs = np.asarray(coeffs, dtype=float)

    # Trim trailing near-zeros to get actual degree
    deg = len(coeffs) - 1
    while deg > 0 and abs(coeffs[deg]) < 1e-12:
        deg -= 1

    if deg <= 0:
        return np.array([])
    elif deg == 1:
        root = -coeffs[0] / coeffs[1]
        return np.array([root]) if 0 <= root <= 1 else np.array([])
    elif deg == 2:
        roots = _quadratic_roots_in_01(coeffs[0], coeffs[1], coeffs[2])
    else:
        # np.roots expects descending order (highest power first)
        eps = 1e-10
        all_roots = np.roots(coeffs[deg::-1])
        real_mask = np.abs(all_roots.imag) < eps
        real_roots = all_roots[real_mask].real
        in_range = (real_roots >= -eps) & (real_roots <= 1 + eps)
        roots = np.clip(real_roots[in_range], 0, 1)

    return np.sort(roots)

