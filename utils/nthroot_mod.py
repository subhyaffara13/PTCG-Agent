
def nthroot_mod(a, n, p, all_roots=False):
    """
    Find the solutions to ``x**n = a mod p``.

    Parameters
    ==========

    a : integer
    n : positive integer
    p : positive integer
    all_roots : if False returns the smallest root, else the list of roots

    Returns
    =======

        list[int] | int | None :
            solutions to ``x**n = a mod p``.
            The table of the output type is:

            ========== ========== ==========
            all_roots  has roots  Returns
            ========== ========== ==========
            True       Yes        list[int]
            True       No         []
            False      Yes        int
            False      No         None
            ========== ========== ==========

    Raises
    ======

        ValueError
            If ``a``, ``n`` or ``p`` is not integer.
            If ``n`` or ``p`` is not positive.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import nthroot_mod
    >>> nthroot_mod(11, 4, 19)
    8
    >>> nthroot_mod(11, 4, 19, True)
    [8, 11]
    >>> nthroot_mod(68, 3, 109)
    23

    References
    ==========

    .. [1] P. Hackman "Elementary Number Theory" (2009), page 76

    """
    a = a % p
    a, n, p = as_int(a), as_int(n), as_int(p)

    if n < 1:
        raise ValueError("n should be positive")
    if p < 1:
        raise ValueError("p should be positive")
    if n == 1:
        return [a] if all_roots else a
    if n == 2:
        return sqrt_mod(a, p, all_roots)
    base = []
    prime_power = []
    for q, e in factorint(p).items():
        tot_roots = _nthroot_mod_prime_power(a, n, q, e)
        if not tot_roots:
            return [] if all_roots else None
        prime_power.append(q**e)
        base.append(sorted(tot_roots))
    P, E, S = gf_crt1(prime_power, ZZ)
    ret = sorted(map(int, {gf_crt2(c, prime_power, P, E, S, ZZ)
                           for c in product(*base)}))
    if all_roots:
        return ret
    if ret:
        return ret[0]

