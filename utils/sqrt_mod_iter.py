
def sqrt_mod_iter(a, p, domain=int):
    """
    Iterate over solutions to ``x**2 = a mod p``.

    Parameters
    ==========

    a : integer
    p : positive integer
    domain : integer domain, ``int``, ``ZZ`` or ``Integer``

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import sqrt_mod_iter
    >>> list(sqrt_mod_iter(11, 43))
    [21, 22]

    See Also
    ========

    sqrt_mod : Same functionality, but you want a sorted list or only one solution.

    """
    a, p = as_int(a), abs(as_int(p))
    v = []
    pv = []
    _product = product
    for px, ex in factorint(p).items():
        if a % px:
            # `len(rx)` is at most 4
            rx = _sqrt_mod_prime_power(a, px, ex)
        else:
            # `len(list(rx))` can be assumed to be large.
            # The `itertools.product` is disadvantageous in terms of memory usage.
            # It is also inferior to iproduct in speed if not all Cartesian products are needed.
            rx = _sqrt_mod1(a, px, ex)
            _product = iproduct
        if not rx:
            return
        v.append(rx)
        pv.append(px**ex)
    if len(v) == 1:
        yield from map(domain, v[0])
    else:
        mm, e, s = gf_crt1(pv, ZZ)
        for vx in _product(*v):
            yield domain(gf_crt2(vx, pv, mm, e, s, ZZ))

