
def _rs_series(expr, series_rs, a, prec):
    # TODO Use _parallel_dict_from_expr instead of sring as sring is
    # inefficient. For details, read the todo in sring.
    args = expr.args
    R = series_rs.ring

    # expr does not contain any function to be expanded
    if not any(arg.has(Function) for arg in args) and not expr.is_Function:
        return series_rs

    if not expr.has(a):
        return series_rs

    elif expr.is_Function:
        arg = args[0]
        if len(args) > 1:
            raise NotImplementedError
        R1, series = sring(arg, domain=QQ, expand=False, series=True)
        series_inner = _rs_series(arg, series, a, prec)

        # Why do we need to compose these three rings?
        #
        # We want to use a simple domain (like ``QQ`` or ``RR``) but they don't
        # support symbolic coefficients. We need a ring that for example lets
        # us have `sin(1)` and `cos(1)` as coefficients if we are expanding
        # `sin(x + 1)`. The ``EX`` domain allows all symbolic coefficients, but
        # that makes it very complex and hence slow.
        #
        # To solve this problem, we add only those symbolic elements as
        # generators to our ring, that we need. Here, series_inner might
        # involve terms like `sin(4)`, `exp(a)`, etc, which are not there in
        # R1 or R. Hence, we compose these three rings to create one that has
        # the generators of all three.
        R = R.compose(R1).compose(series_inner.ring)
        series_inner = series_inner.set_ring(R)
        series = eval(_convert_func[str(expr.func)])(series_inner,
            R(a), prec)
        return series

    elif expr.is_Mul:
        n = len(args)
        for arg in args:    # XXX Looks redundant
            if not arg.is_Number:
                R1, _ = sring(arg, expand=False, series=True)
                R = R.compose(R1)
        min_pows = list(map(rs_min_pow, args, [R(arg) for arg in args],
            [a]*len(args)))
        sum_pows = sum(min_pows)
        series = R(1)

        for i in range(n):
            _series = _rs_series(args[i], R(args[i]), a, ceiling(prec
                - sum_pows + min_pows[i]))
            R = R.compose(_series.ring)
            _series = _series.set_ring(R)
            series = series.set_ring(R)
            series *= _series
        series = rs_trunc(series, R(a), prec)
        return series

    elif expr.is_Add:
        n = len(args)
        series = R(0)
        for i in range(n):
            _series = _rs_series(args[i], R(args[i]), a, prec)
            R = R.compose(_series.ring)
            _series = _series.set_ring(R)
            series = series.set_ring(R)
            series += _series
        return series

    elif expr.is_Pow:
        R1, _ = sring(expr.base, domain=QQ, expand=False, series=True)
        R = R.compose(R1)
        series_inner = _rs_series(expr.base, R(expr.base), a, prec)
        return rs_pow(series_inner, expr.exp, series_inner.ring(a), prec)

    # The `is_constant` method is buggy hence we check it at the end.
    # See issue #9786 for details.
    elif isinstance(expr, Expr) and expr.is_constant():
        return sring(expr, domain=QQ, expand=False, series=True)[1]

    else:
        raise NotImplementedError

