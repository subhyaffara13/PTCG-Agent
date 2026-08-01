
def _primitive_root_prime_power_iter(p, e):
    r""" Generates the primitive roots of `p^e`.

    Explanation
    ===========

    Let ``g`` be the primitive root of ``p``.
    If `g^{p-1} \not\equiv 1 \pmod{p^2}`, then ``g`` is primitive root of `p^e`.
    Thus, if we find a primitive root ``g`` of ``p``,
    then `g, g+p, g+2p, \ldots, g+(p-1)p` are primitive roots of `p^2` except one.
    That one satisfies `\hat{g}^{p-1} \equiv 1 \pmod{p^2}`.
    If ``h`` is the primitive root of `p^2`,
    then `h, h+p^2, h+2p^2, \ldots, h+(p^{e-2}-1)p^e` are primitive roots of `p^e`.

    Parameters
    ==========

    p : odd prime
    e : positive integer

    Yields
    ======

    int
        the primitive roots of `p^e`

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _primitive_root_prime_power_iter
    >>> sorted(_primitive_root_prime_power_iter(5, 2))
    [2, 3, 8, 12, 13, 17, 22, 23]

    """
    if e == 1:
        yield from _primitive_root_prime_iter(p)
    else:
        p2 = p**2
        for g in _primitive_root_prime_iter(p):
            t = (g - pow(g, 2 - p, p2)) % p2
            for k in range(0, p2, p):
                if k != t:
                    yield from (g + k + m for m in range(0, p**e, p2))

