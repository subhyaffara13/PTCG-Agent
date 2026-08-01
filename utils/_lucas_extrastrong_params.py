
def _lucas_extrastrong_params(n):
    """Calculates the "extra strong" parameters (D, P, Q) for n.

    Parameters
    ==========

    n : int
        positive odd integer

    Returns
    =======

    D, P, Q: "extra strong" parameters.
             ``(0, 0, 0)`` if we find a nontrivial divisor of ``n``.

    Examples
    ========

    >>> from sympy.ntheory.primetest import _lucas_extrastrong_params
    >>> _lucas_extrastrong_params(101)
    (12, 4, 1)
    >>> _lucas_extrastrong_params(15)
    (0, 0, 0)

    References
    ==========
    .. [1] OEIS A217719: Extra Strong Lucas Pseudoprimes
           https://oeis.org/A217719
    .. [2] https://en.wikipedia.org/wiki/Lucas_pseudoprime

    """
    for P in count(3):
        D = P**2 - 4
        j = jacobi(D, n)
        if j == -1:
            return (D, P, 1)
        elif j == 0 and D % n:
            return (0, 0, 0)

