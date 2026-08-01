
def _process_summations(sum_bound, *args):
    """Substitute oo (infinity) in the lower/upper bounds of a summation with
    some integer number.

    Parameters
    ==========

    sum_bound : int
        oo will be substituted with this integer number.
    *args : list/tuple
        pre-processed arguments of the form (expr, range, ...)

    Notes
    =====
    Let's consider the following summation: ``Sum(1 / x**2, (x, 1, oo))``.
    The current implementation of lambdify (SymPy 1.12 at the time of
    writing this) will create something of this form:
    ``sum(1 / x**2 for x in range(1, INF))``
    The problem is that ``type(INF)`` is float, while ``range`` requires
    integers: the evaluation fails.
    Instead of modifying ``lambdify`` (which requires a deep knowledge), just
    replace it with some integer number.
    """
    def new_bound(t, bound):
        if (not t.is_number) or t.is_finite:
            return t
        if sign(t) >= 0:
            return bound
        return -bound

    args = list(args)
    expr = args[0]

    # select summations whose lower/upper bound is infinity
    w = Wild("w", properties=[
        lambda t: isinstance(t, Sum),
        lambda t: any((not a[1].is_finite) or (not a[2].is_finite) for i, a in enumerate(t.args) if i > 0)
    ])

    for t in list(expr.find(w)):
        sums_args = list(t.args)
        for i, a in enumerate(sums_args):
            if i > 0:
                sums_args[i] = (a[0], new_bound(a[1], sum_bound),
                    new_bound(a[2], sum_bound))
        s = Sum(*sums_args)
        expr = expr.subs(t, s)
    args[0] = expr
    return args

