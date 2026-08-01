
def reduced(f, G, *gens, **args):
    """
    Reduces a polynomial ``f`` modulo a set of polynomials ``G``.

    Given a polynomial ``f`` and a set of polynomials ``G = (g_1, ..., g_n)``,
    computes a set of quotients ``q = (q_1, ..., q_n)`` and the remainder ``r``
    such that ``f = q_1*g_1 + ... + q_n*g_n + r``, where ``r`` vanishes or ``r``
    is a completely reduced polynomial with respect to ``G``.

    Examples
    ========

    >>> from sympy import reduced
    >>> from sympy.abc import x, y

    >>> reduced(2*x**4 + y**2 - x**2 + y**3, [x**3 - x, y**3 - y])
    ([2*x, 1], x**2 + y**2 + y)

    """
    options.allowed_flags(args, ['polys', 'auto'])

    try:
        polys, opt = parallel_poly_from_expr([f] + list(G), *gens, **args)
    except PolificationFailed as exc:
        raise ComputationFailed('reduced', 0, exc)

    domain = opt.domain
    retract = False

    if opt.auto and domain.is_Ring and not domain.is_Field:
        opt = opt.clone({"domain": domain.get_field()})
        retract = True

    from sympy.polys.rings import xring
    _ring, _ = xring(opt.gens, opt.domain, opt.order)

    for i, poly in enumerate(polys):
        poly = poly.set_domain(opt.domain).rep.to_dict()
        polys[i] = _ring.from_dict(poly)

    Q, r = polys[0].div(polys[1:])

    Q = [Poly._from_dict(dict(q), opt) for q in Q]
    r = Poly._from_dict(dict(r), opt)

    if retract:
        try:
            _Q, _r = [q.to_ring() for q in Q], r.to_ring()
        except CoercionFailed:
            pass
        else:
            Q, r = _Q, _r

    if not opt.polys:
        return [q.as_expr() for q in Q], r.as_expr()
    else:
        return Q, r

