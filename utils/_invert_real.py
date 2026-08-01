
def _invert_real(f, g_ys, symbol):
    """Helper function for _invert."""

    if f == symbol or g_ys is S.EmptySet:
        return (symbol, g_ys)

    n = Dummy('n', real=True)

    if isinstance(f, exp) or (f.is_Pow and f.base == S.Exp1):
        return _invert_real(f.exp,
                            imageset(Lambda(n, log(n)), g_ys),
                            symbol)

    if hasattr(f, 'inverse') and f.inverse() is not None and not isinstance(f, (
            TrigonometricFunction,
            HyperbolicFunction,
            )):
        if len(f.args) > 1:
            raise ValueError("Only functions with one argument are supported.")
        return _invert_real(f.args[0],
                            imageset(Lambda(n, f.inverse()(n)), g_ys),
                            symbol)

    if isinstance(f, Abs):
        return _invert_abs(f.args[0], g_ys, symbol)

    if f.is_Add:
        # f = g + h
        g, h = f.as_independent(symbol)
        if g is not S.Zero:
            return _invert_real(h, imageset(Lambda(n, n - g), g_ys), symbol)

    if f.is_Mul:
        # f = g*h
        g, h = f.as_independent(symbol)

        if g is not S.One:
            return _invert_real(h, imageset(Lambda(n, n/g), g_ys), symbol)

    if f.is_Pow:
        base, expo = f.args
        base_has_sym = base.has(symbol)
        expo_has_sym = expo.has(symbol)

        if not expo_has_sym:

            if expo.is_rational:
                num, den = expo.as_numer_denom()

                if den % 2 == 0 and num % 2 == 1 and den.is_zero is False:
                    # Here we have f(x)**(num/den) = y
                    # where den is nonzero and even and y is an element
                    # of the set g_ys.
                    # den is even, so we are only interested in the cases
                    # where both f(x) and y are positive.
                    # Restricting y to be positive (using the set g_ys_pos)
                    # means that y**(den/num) is always positive.
                    # Therefore it isn't necessary to also constrain f(x)
                    # to be positive because we are only going to
                    # find solutions of f(x) = y**(d/n)
                    # where the rhs is already required to be positive.
                    root = Lambda(n, real_root(n, expo))
                    g_ys_pos = g_ys & Interval(0, oo)
                    res = imageset(root, g_ys_pos)
                    _inv, _set = _invert_real(base, res, symbol)
                    return (_inv, _set)

                if den % 2 == 1:
                    root = Lambda(n, real_root(n, expo))
                    res = imageset(root, g_ys)
                    if num % 2 == 0:
                        neg_res = imageset(Lambda(n, -n), res)
                        return _invert_real(base, res + neg_res, symbol)
                    if num % 2 == 1:
                        return _invert_real(base, res, symbol)

            elif expo.is_irrational:
                root = Lambda(n, real_root(n, expo))
                g_ys_pos = g_ys & Interval(0, oo)
                res = imageset(root, g_ys_pos)
                return _invert_real(base, res, symbol)

            else:
                # indeterminate exponent, e.g. Float or parity of
                # num, den of rational could not be determined
                pass  # use default return

        if not base_has_sym:
            rhs = g_ys.args[0]
            if base.is_positive:
                return _invert_real(expo,
                    imageset(Lambda(n, log(n, base, evaluate=False)), g_ys), symbol)
            elif base.is_negative:
                s, b = integer_log(rhs, base)
                if b:
                    return _invert_real(expo, FiniteSet(s), symbol)
                else:
                    return (expo, S.EmptySet)
            elif base.is_zero:
                one = Eq(rhs, 1)
                if one == S.true:
                    # special case: 0**x - 1
                    return _invert_real(expo, FiniteSet(0), symbol)
                elif one == S.false:
                    return (expo, S.EmptySet)

    if isinstance(f, (TrigonometricFunction, HyperbolicFunction)):
        return _invert_trig_hyp_real(f, g_ys, symbol)

    return (f, g_ys)

