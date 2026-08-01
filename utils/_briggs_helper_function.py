
def _briggs_helper_function(a, k):
    """
    Computes r = a^(1 / (2^k)) - 1.

    This is algorithm (2) of [1]_.
    The purpose is to avoid a danger of subtractive cancellation.
    For more computational efficiency it should probably be cythonized.

    Parameters
    ----------
    a : complex
        A complex number.
    k : int
        A nonnegative integer.

    Returns
    -------
    r : complex
        The value r = a^(1 / (2^k)) - 1 computed with less cancellation.

    Notes
    -----
    The algorithm as formulated in the reference does not handle k=0 or k=1
    correctly, so these are special-cased in this implementation.
    This function is intended to not allow `a` to belong to the closed
    negative real axis, but this constraint is relaxed.

    References
    ----------
    .. [1] Awad H. Al-Mohy (2012)
           "A more accurate Briggs method for the logarithm",
           Numerical Algorithms, 59 : 393--402.

    """
    if k < 0 or int(k) != k:
        raise ValueError('expected a nonnegative integer k')
    if k == 0:
        return a - 1
    elif k == 1:
        return np.sqrt(a) - 1
    else:
        k_hat = k
        if np.angle(a) >= np.pi / 2:
            a = np.sqrt(a)
            k_hat = k - 1
        z0 = a - 1
        a = np.sqrt(a)
        r = 1 + a
        for j in range(1, k_hat):
            a = np.sqrt(a)
            r = r * (1 + a)
        r = z0 / r
        return r

