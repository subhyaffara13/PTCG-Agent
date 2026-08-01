
def _discrete_log_shanks_steps(n, a, b, order=None):
    """
    Baby-step giant-step algorithm for computing the discrete logarithm of
    ``a`` to the base ``b`` modulo ``n``.

    The algorithm is a time-memory trade-off of the method of exhaustive
    search. It uses `O(sqrt(m))` memory, where `m` is the group order.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _discrete_log_shanks_steps
    >>> _discrete_log_shanks_steps(41, 15, 7)
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
        order = n_order(b, n)
    m = sqrt(order) + 1
    T = {}
    x = 1
    for i in range(m):
        T[x] = i
        x = x * b % n
    z = pow(b, -m, n)
    x = a
    for i in range(m):
        if x in T:
            return i * m + T[x]
        x = x * z % n
    raise ValueError("Log does not exist")

