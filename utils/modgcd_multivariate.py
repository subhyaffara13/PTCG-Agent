
def modgcd_multivariate(f, g):
    r"""
    Compute the GCD of two polynomials in `\mathbb{Z}[x_0, \ldots, x_{k-1}]`
    using a modular algorithm.

    The algorithm computes the GCD of two multivariate integer polynomials
    `f` and `g` by calculating the GCD in
    `\mathbb{Z}_p[x_0, \ldots, x_{k-1}]` for suitable primes `p` and then
    reconstructing the coefficients with the Chinese Remainder Theorem. To
    compute the multivariate GCD over `\mathbb{Z}_p` the recursive
    subroutine :func:`_modgcd_multivariate_p` is used. To verify the result in
    `\mathbb{Z}[x_0, \ldots, x_{k-1}]`, trial division is done, but only for
    candidates which are very likely the desired GCD.

    Parameters
    ==========

    f : PolyElement
        multivariate integer polynomial
    g : PolyElement
        multivariate integer polynomial

    Returns
    =======

    h : PolyElement
        GCD of the polynomials `f` and `g`
    cff : PolyElement
        cofactor of `f`, i.e. `\frac{f}{h}`
    cfg : PolyElement
        cofactor of `g`, i.e. `\frac{g}{h}`

    Examples
    ========

    >>> from sympy.polys.modulargcd import modgcd_multivariate
    >>> from sympy.polys import ring, ZZ

    >>> R, x, y = ring("x, y", ZZ)

    >>> f = x**2 - y**2
    >>> g = x**2 + 2*x*y + y**2

    >>> h, cff, cfg = modgcd_multivariate(f, g)
    >>> h, cff, cfg
    (x + y, x - y, x + y)

    >>> cff * h == f
    True
    >>> cfg * h == g
    True

    >>> R, x, y, z = ring("x, y, z", ZZ)

    >>> f = x*z**2 - y*z**2
    >>> g = x**2*z + z

    >>> h, cff, cfg = modgcd_multivariate(f, g)
    >>> h, cff, cfg
    (z, x*z - y*z, x**2 + 1)

    >>> cff * h == f
    True
    >>> cfg * h == g
    True

    References
    ==========

    1. [Monagan00]_
    2. [Brown71]_

    See also
    ========

    _modgcd_multivariate_p

    """
    assert f.ring == g.ring and f.ring.domain.is_ZZ

    result = _trivial_gcd(f, g)
    if result is not None:
        return result

    ring = f.ring
    k = ring.ngens

    # divide out integer content
    cf, f = f.primitive()
    cg, g = g.primitive()
    ch = ring.domain.gcd(cf, cg)

    gamma = ring.domain.gcd(f.LC, g.LC)

    badprimes = ring.domain.one
    for i in range(k):
        badprimes *= ring.domain.gcd(_swap(f, i).LC, _swap(g, i).LC)

    degbound = [min(fdeg, gdeg) for fdeg, gdeg in zip(f.degrees(), g.degrees())]
    contbound = list(degbound)

    m = 1
    p = 1

    while True:
        p = nextprime(p)
        while badprimes % p == 0:
            p = nextprime(p)

        fp = f.trunc_ground(p)
        gp = g.trunc_ground(p)

        try:
            # monic GCD of fp, gp in Z_p[x_0, ..., x_{k-2}, y]
            hp = _modgcd_multivariate_p(fp, gp, p, degbound, contbound)
        except ModularGCDFailed:
            m = 1
            continue

        if hp is None:
            continue

        hp = hp.mul_ground(gamma).trunc_ground(p)
        if m == 1:
            m = p
            hlastm = hp
            continue

        hm = _chinese_remainder_reconstruction_multivariate(hp, hlastm, p, m)
        m *= p

        if not hm == hlastm:
            hlastm = hm
            continue

        h = hm.primitive()[1]
        fquo, frem = f.div(h)
        gquo, grem = g.div(h)
        if not frem and not grem:
            if h.LC < 0:
                ch = -ch
            h = h.mul_ground(ch)
            cff = fquo.mul_ground(cf // ch)
            cfg = gquo.mul_ground(cg // ch)
            return h, cff, cfg

