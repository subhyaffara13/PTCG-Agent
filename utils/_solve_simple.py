
def _solve_simple(f, x, DE, g, k):
    """Converts DE into RE and solves using :func:`rsolve`."""
    from sympy.solvers import rsolve

    RE = hyper_re(DE, g, k)

    init = {}
    for i in range(len(Add.make_args(RE))):
        if i:
            f = f.diff(x)
        init[g(k).subs(k, i)] = f.limit(x, 0) / factorial(i)

    sol = rsolve(RE, g(k), init)

    if sol:
        return (sol, S.Zero, S.Zero)

