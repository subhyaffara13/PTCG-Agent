
def _solve_explike_DE(f, x, DE, g, k):
    """Solves DE with constant coefficients."""
    from sympy.solvers import rsolve

    for t in Add.make_args(DE):
        coeff, d = t.as_independent(g)
        if coeff.free_symbols:
            return

    RE = exp_re(DE, g, k)

    init = {}
    for i in range(len(Add.make_args(RE))):
        if i:
            f = f.diff(x)
        init[g(k).subs(k, i)] = f.limit(x, 0)

    sol = rsolve(RE, g(k), init)

    if sol:
        return (sol / factorial(k), S.Zero, S.Zero)

