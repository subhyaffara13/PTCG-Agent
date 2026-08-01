
def _invert_complex(f, g_ys, symbol):
    """Helper function for _invert."""

    if f == symbol or g_ys is S.EmptySet:
        return (symbol, g_ys)

    n = Dummy('n')

    if f.is_Add:
        # f = g + h
        g, h = f.as_independent(symbol)
        if g is not S.Zero:
            return _invert_complex(h, imageset(Lambda(n, n - g), g_ys), symbol)

    if f.is_Mul:
        # f = g*h
        g, h = f.as_independent(symbol)

        if g is not S.One:
            if g in {S.NegativeInfinity, S.ComplexInfinity, S.Infinity}:
                return (h, S.EmptySet)
            return _invert_complex(h, imageset(Lambda(n, n/g), g_ys), symbol)

    if f.is_Pow:
        base, expo = f.args
        # special case: g**r = 0
        # Could be improved like `_invert_real` to handle more general cases.
        if expo.is_Rational and g_ys == FiniteSet(0):
            if expo.is_positive:
                return _invert_complex(base, g_ys, symbol)

    if hasattr(f, 'inverse') and f.inverse() is not None and \
       not isinstance(f, TrigonometricFunction) and \
       not isinstance(f, HyperbolicFunction) and \
       not isinstance(f, exp):
        if len(f.args) > 1:
            raise ValueError("Only functions with one argument are supported.")
        return _invert_complex(f.args[0],
                               imageset(Lambda(n, f.inverse()(n)), g_ys), symbol)

    if isinstance(f, exp) or (f.is_Pow and f.base == S.Exp1):
        if isinstance(g_ys, ImageSet):
            # can solve up to `(d*exp(exp(...(exp(a*x + b))...) + c)` format.
            # Further can be improved to `(d*exp(exp(...(exp(a*x**n + b*x**(n-1) + ... + f))...) + c)`.
            g_ys_expr = g_ys.lamda.expr
            g_ys_vars = g_ys.lamda.variables
            k = Dummy('k{}'.format(len(g_ys_vars)))
            g_ys_vars_1 = (k,) + g_ys_vars
            exp_invs = Union(*[imageset(Lambda((g_ys_vars_1,), (I*(2*k*pi + arg(g_ys_expr))
                                         + log(Abs(g_ys_expr)))), S.Integers**(len(g_ys_vars_1)))])
            return _invert_complex(f.exp, exp_invs, symbol)

        elif isinstance(g_ys, FiniteSet):
            exp_invs = Union(*[imageset(Lambda(n, I*(2*n*pi + arg(g_y)) +
                                               log(Abs(g_y))), S.Integers)
                               for g_y in g_ys if g_y != 0])
            return _invert_complex(f.exp, exp_invs, symbol)

    if isinstance(f, (TrigonometricFunction, HyperbolicFunction)):
        return _invert_trig_hyp_complex(f, g_ys, symbol)

    return (f, g_ys)

