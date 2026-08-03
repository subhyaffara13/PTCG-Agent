from typing import Union

def _solve_trig2(f, symbol, domain):
    """Secondary helper to solve trigonometric equations,
    called when first helper fails """
    f = trigsimp(f)
    f_original = f
    trig_functions = f.atoms(sin, cos, tan, sec, cot, csc)
    trig_arguments = [e.args[0] for e in trig_functions]
    denominators = []
    numerators = []

    # todo: This solver can be extended to hyperbolics if the
    # analogous change of variable to tanh (instead of tan)
    # is used.
    if not trig_functions:
        return ConditionSet(symbol, Eq(f_original, 0), domain)

    # todo: The pre-processing below (extraction of numerators, denominators,
    # gcd, lcm, mu, etc.) should be updated to the enhanced version in
    # _solve_trig1. (See #19507)
    for ar in trig_arguments:
        try:
            poly_ar = Poly(ar, symbol)
        except PolynomialError:
            raise ValueError("give up, we cannot solve if this is not a polynomial in x")
        if poly_ar.degree() > 1:  # degree >1 still bad
            raise ValueError("degree of variable inside polynomial should not exceed one")
        if poly_ar.degree() == 0:  # degree 0, don't care
            continue
        c = poly_ar.all_coeffs()[0]   # got the coefficient of 'symbol'
        try:
            numerators.append(Rational(c).p)
            denominators.append(Rational(c).q)
        except TypeError:
            return ConditionSet(symbol, Eq(f_original, 0), domain)

    x = Dummy('x')

    mu = Rational(2)*number_lcm(*denominators)/number_gcd(*numerators)
    f = f.subs(symbol, mu*x)
    f = f.rewrite(tan)
    f = expand_trig(f)
    f = together(f)

    g, h = fraction(f)
    y = Dummy('y')
    g, h = g.expand(), h.expand()
    g, h = g.subs(tan(x), y), h.subs(tan(x), y)

    if g.has(x) or h.has(x):
        return ConditionSet(symbol, Eq(f_original, 0), domain)
    solns = solveset(g, y, S.Reals) - solveset(h, y, S.Reals)

    if isinstance(solns, FiniteSet):
        result = Union(*[invert_real(tan(symbol/mu), s, symbol)[1]
                       for s in solns])
        dsol = invert_real(tan(symbol/mu), oo, symbol)[1]
        if degree(h) > degree(g):                   # If degree(denom)>degree(num) then there
            result = Union(result, dsol)            # would be another sol at Lim(denom-->oo)
        return Intersection(result, domain)
    elif solns is S.EmptySet:
        return S.EmptySet
    else:
        return ConditionSet(symbol, Eq(f_original, 0), S.Reals)

