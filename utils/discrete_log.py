
def discrete_log(n, a, b, order=None, prime_order=None):
    """
    Compute the discrete logarithm of ``a`` to the base ``b`` modulo ``n``.

    This is a recursive function to reduce the discrete logarithm problem in
    cyclic groups of composite order to the problem in cyclic groups of prime
    order.

    It employs different algorithms depending on the problem (subgroup order
    size, prime order or not):

        * Trial multiplication
        * Baby-step giant-step
        * Pollard's Rho
        * Index Calculus
        * Pohlig-Hellman

    Examples
    ========

    >>> from sympy.ntheory import discrete_log
    >>> discrete_log(41, 15, 7)
    3

    References
    ==========

    .. [1] https://mathworld.wolfram.com/DiscreteLogarithm.html
    .. [2] "Handbook of applied cryptography", Menezes, A. J., Van, O. P. C., &
        Vanstone, S. A. (1997).

    """
    from math import sqrt, log
    n, a, b = as_int(n), as_int(a), as_int(b)

    if n < 1:
        raise ValueError("n should be positive")
    if n == 1:
        return 0

    if order is None:
        # Compute the order and its factoring in one pass
        # order = totient(n), factors = factorint(order)
        factors = {}
        for px, kx in factorint(n).items():
            if kx > 1:
                if px in factors:
                    factors[px] += kx - 1
                else:
                    factors[px] = kx - 1
            for py, ky in factorint(px - 1).items():
                if py in factors:
                    factors[py] += ky
                else:
                    factors[py] = ky
        order = 1
        for px, kx in factors.items():
            order *= px**kx
        # Now the `order` is the order of the group and factors = factorint(order)
        # The order of `b` divides the order of the group.
        order_factors = {}
        for p, e in factors.items():
            i = 0
            for _ in range(e):
                if pow(b, order // p, n) == 1:
                    order //= p
                    i += 1
                else:
                    break
            if i < e:
                order_factors[p] = e - i

    if prime_order is None:
        prime_order = isprime(order)

    if order < 1000:
        return _discrete_log_trial_mul(n, a, b, order)
    elif prime_order:
        # Shanks and Pollard rho are O(sqrt(order)) while index calculus is O(exp(2*sqrt(log(n)log(log(n)))))
        # we compare the expected running times to determine the algorithm which is expected to be faster
        if 4*sqrt(log(n)*log(log(n))) < log(order) - 10:  # the number 10 was determined experimental
            return _discrete_log_index_calculus(n, a, b, order)
        elif order < 1000000000000:
            # Shanks seems typically faster, but uses O(sqrt(order)) memory
            return _discrete_log_shanks_steps(n, a, b, order)
        return _discrete_log_pollard_rho(n, a, b, order)

    return _discrete_log_pohlig_hellman(n, a, b, order, order_factors)

