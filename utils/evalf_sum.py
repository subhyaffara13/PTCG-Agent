
def evalf_sum(expr: 'Sum', prec: int, options: OPT_DICT) -> TMP_RES:
    from .numbers import Float
    if 'subs' in options:
        expr = expr.subs(options['subs']) # type: ignore
    func = expr.function
    limits = expr.limits
    if len(limits) != 1 or len(limits[0]) != 3:
        raise NotImplementedError
    if func.is_zero:
        return None, None, prec, None
    prec2 = prec + 10
    try:
        n, a, b = limits[0]
        if b is not S.Infinity or a is S.NegativeInfinity or a != int(a):
            raise NotImplementedError
        # Use fast hypergeometric summation if possible
        v = hypsum(func, n, int(a), prec2)
        delta = prec - fastlog(v)
        if fastlog(v) < -10:
            v = hypsum(func, n, int(a), delta)
        return v, None, min(prec, delta), None
    except NotImplementedError:
        # Euler-Maclaurin summation for general series
        eps = Float(2.0)**(-prec)
        for i in range(1, 5):
            m = n = 2**i * prec
            s, err = expr.euler_maclaurin(m=m, n=n, eps=eps,
                eval_integral=False)
            err = err.evalf()
            if err is S.NaN:
                raise NotImplementedError
            if err <= eps:
                break
        err = fastlog(evalf(abs(err), 20, options)[0])
        re, im, re_acc, im_acc = evalf(s, prec2, options)
        if re_acc is None:
            re_acc = -err
        if im_acc is None:
            im_acc = -err
        return re, im, re_acc, im_acc

