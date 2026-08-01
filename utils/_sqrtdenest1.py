
def _sqrtdenest1(expr, denester=True):
    """Return denested expr after denesting with simpler methods or, that
    failing, using the denester."""

    from sympy.simplify.simplify import radsimp

    if not is_sqrt(expr):
        return expr

    a = expr.base
    if a.is_Atom:
        return expr
    val = _sqrt_match(a)
    if not val:
        return expr

    a, b, r = val
    # try a quick numeric denesting
    d2 = _mexpand(a**2 - b**2*r)
    if d2.is_Rational:
        if d2.is_positive:
            z = _sqrt_numeric_denest(a, b, r, d2)
            if z is not None:
                return z
        else:
            # fourth root case
            # sqrtdenest(sqrt(3 + 2*sqrt(3))) =
            # sqrt(2)*3**(1/4)/2 + sqrt(2)*3**(3/4)/2
            dr2 = _mexpand(-d2*r)
            dr = sqrt(dr2)
            if dr.is_Rational:
                z = _sqrt_numeric_denest(_mexpand(b*r), a, r, dr2)
                if z is not None:
                    return z/root(r, 4)

    else:
        z = _sqrt_symbolic_denest(a, b, r)
        if z is not None:
            return z

    if not denester or not is_algebraic(expr):
        return expr

    res = sqrt_biquadratic_denest(expr, a, b, r, d2)
    if res:
        return res

    # now call to the denester
    av0 = [a, b, r, d2]
    z = _denester([radsimp(expr**2)], av0, 0, sqrt_depth(expr))[0]
    if av0[1] is None:
        return expr
    if z is not None:
        if sqrt_depth(z) == sqrt_depth(expr) and count_ops(z) > count_ops(expr):
            return expr
        return z
    return expr

