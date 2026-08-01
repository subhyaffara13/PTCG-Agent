
def _transform_DE_RE(DE, g, k, order, syms):
    """Converts DE with free parameters into RE of hypergeometric type."""
    from sympy.solvers.solveset import linsolve

    RE = hyper_re(DE, g, k)

    eq = [RE.coeff(g(k + i)) for i in range(1, order)]
    sol = dict(zip(syms, (i for s in linsolve(eq, list(syms)) for i in s)))
    if sol:
        m = Wild('m')
        RE = RE.subs(sol)
        RE = RE.factor().as_numer_denom()[0].collect(g(k + m))
        RE = RE.as_coeff_mul(g)[1][0]
        for i in range(order):  # smallest order should be g(k)
            if RE.coeff(g(k + i)) and i:
                RE = RE.subs(k, k - i)
                break
    return RE

