
def _primitive_root_prime_power2_iter(p, e):
    r""" Generates the primitive roots of `2p^e`.

    Explanation
    ===========

    If ``g`` is the primitive root of ``p**e``,
    then the odd one of ``g`` and ``g+p**e`` is the primitive root of ``2*p**e``.

    Parameters
    ==========

    p : odd prime
    e : positive integer

    Yields
    ======

    int
        the primitive roots of `2p^e`

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _primitive_root_prime_power2_iter
    >>> sorted(_primitive_root_prime_power2_iter(5, 2))
    [3, 13, 17, 23, 27, 33, 37, 47]

    """
    for g in _primitive_root_prime_power_iter(p, e):
        if g % 2 == 1:
            yield g
        else:
            yield g + p**e

