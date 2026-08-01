
def _choose_factor(factors, x, v, dom=QQ, prec=200, bound=5):
    """
    Return a factor having root ``v``
    It is assumed that one of the factors has root ``v``.
    """

    if isinstance(factors[0], tuple):
        factors = [f[0] for f in factors]
    if len(factors) == 1:
        return factors[0]

    prec1 = 10
    points = {}
    symbols = dom.symbols if hasattr(dom, 'symbols') else []
    while prec1 <= prec:
        # when dealing with non-Rational numbers we usually evaluate
        # with `subs` argument but we only need a ballpark evaluation
        fe = [f.as_expr().xreplace({x:v}) for f in factors]
        if v.is_number:
            fe = [f.n(prec) for f in fe]

        # assign integers [0, n) to symbols (if any)
        for n in subsets(range(bound), k=len(symbols), repetition=True):
            for s, i in zip(symbols, n):
                points[s] = i

            # evaluate the expression at these points
            candidates = [(abs(f.subs(points).n(prec1)), i)
                for i,f in enumerate(fe)]

            # if we get invalid numbers (e.g. from division by zero)
            # we try again
            if any(i in _illegal for i, _ in candidates):
                continue

            # find the smallest two -- if they differ significantly
            # then we assume we have found the factor that becomes
            # 0 when v is substituted into it
            can = sorted(candidates)
            (a, ix), (b, _) = can[:2]
            if b > a * 10**6:  # XXX what to use?
                return factors[ix]

        prec1 *= 2

    raise NotImplementedError("multiple candidates for the minimal polynomial of %s" % v)

