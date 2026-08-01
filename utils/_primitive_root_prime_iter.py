
def _primitive_root_prime_iter(p):
    r""" Generates the primitive roots for a prime ``p``.

    Explanation
    ===========

    The primitive roots generated are not necessarily sorted.
    However, the first one is the smallest primitive root.

    Find the element whose order is ``p-1`` from the smaller one.
    If we can find the first primitive root ``g``, we can use the following theorem.

    .. math ::
        \operatorname{ord}(g^k) = \frac{\operatorname{ord}(g)}{\gcd(\operatorname{ord}(g), k)}

    From the assumption that `\operatorname{ord}(g)=p-1`,
    it is a necessary and sufficient condition for
    `\operatorname{ord}(g^k)=p-1` that `\gcd(p-1, k)=1`.

    Parameters
    ==========

    p : odd prime

    Yields
    ======

    int
        the primitive roots of ``p``

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _primitive_root_prime_iter
    >>> sorted(_primitive_root_prime_iter(19))
    [2, 3, 10, 13, 14, 15]

    References
    ==========

    .. [1] W. Stein "Elementary Number Theory" (2011), page 44

    """
    if p == 3:
        yield 2
        return
    # Let p = +-1 (mod 4a). Legendre symbol (a/p) = 1, so `a` is not the primitive root.
    # Corollary : If p = +-1 (mod 8), then 2 is not the primitive root of p.
    g_min = 3 if p % 8 in [1, 7] else 2
    if p < 41:
        # small case
        g = 5 if p == 23 else g_min
    else:
        v = [(p - 1) // i for i in factorint(p - 1).keys()]
        for g in range(g_min, p):
            if all(pow(g, pw, p) != 1 for pw in v):
                break
    yield g
    # g**k is the primitive root of p iff gcd(p - 1, k) = 1
    for k in range(3, p, 2):
        if gcd(p - 1, k) == 1:
            yield pow(g, k, p)

