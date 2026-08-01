
def _rsolve_hypergeometric(f, x, P, Q, k, m):
    """
    Recursive wrapper to rsolve_hypergeometric.

    Explanation
    ===========

    Returns a Tuple of (formula, series independent terms,
    maximum power of x in independent terms) if successful
    otherwise ``None``.

    See :func:`rsolve_hypergeometric` for details.
    """
    from sympy.polys import lcm, roots
    from sympy.integrals import integrate

    # transformation - c
    proots, qroots = roots(P, k), roots(Q, k)
    all_roots = dict(proots)
    all_roots.update(qroots)
    scale = lcm([r.as_numer_denom()[1] for r, t in all_roots.items()
                 if r.is_rational])
    f, P, Q, m = _transformation_c(f, x, P, Q, k, m, scale)

    # transformation - a
    qroots = roots(Q, k)
    if qroots:
        k_min = Min(*qroots.keys())
    else:
        k_min = S.Zero
    shift = k_min + m
    f, P, Q, m = _transformation_a(f, x, P, Q, k, m, shift)

    l = (x*f).limit(x, 0)
    if not isinstance(l, Limit) and l != 0:  # Ideally should only be l != 0
        return None

    qroots = roots(Q, k)
    if qroots:
        k_max = Max(*qroots.keys())
    else:
        k_max = S.Zero

    ind, mp = S.Zero, -oo
    for i in range(k_max + m + 1):
        r = f.diff(x, i).limit(x, 0) / factorial(i)
        if r.is_finite is False:
            old_f = f
            f, P, Q, m = _transformation_a(f, x, P, Q, k, m, i)
            f, P, Q, m = _transformation_e(f, x, P, Q, k, m)
            sol, ind, mp = _rsolve_hypergeometric(f, x, P, Q, k, m)
            sol = _apply_integrate(sol, x, k)
            sol = _apply_shift(sol, i)
            ind = integrate(ind, x)
            ind += (old_f - ind).limit(x, 0)  # constant of integration
            mp += 1
            return sol, ind, mp
        elif r:
            ind += r*x**(i + shift)
            pow_x = Rational((i + shift), scale)
            if pow_x > mp:
                mp = pow_x  # maximum power of x
    ind = ind.subs(x, x**(1/scale))

    sol = _compute_formula(f, x, P, Q, k, m, k_max)
    sol = _apply_shift(sol, shift)
    sol = _apply_scale(sol, scale)

    return sol, ind, mp

