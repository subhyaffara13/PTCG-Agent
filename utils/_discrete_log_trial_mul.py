
def _discrete_log_trial_mul(n, a, b, order=None):
    """
    Trial multiplication algorithm for computing the discrete logarithm of
    ``a`` to the base ``b`` modulo ``n``.

    The algorithm finds the discrete logarithm using exhaustive search. This
    naive method is used as fallback algorithm of ``discrete_log`` when the
    group order is very small. The value ``n`` must be greater than 1.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _discrete_log_trial_mul
    >>> _discrete_log_trial_mul(41, 15, 7)
    3

    See Also
    ========

    discrete_log

    References
    ==========

    .. [1] "Handbook of applied cryptography", Menezes, A. J., Van, O. P. C., &
        Vanstone, S. A. (1997).
    """
    a %= n
    b %= n
    if order is None:
        order = n
    x = 1
    for i in range(order):
        if x == a:
            return i
        x = x * b % n
    raise ValueError("Log does not exist")

