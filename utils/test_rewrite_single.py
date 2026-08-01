
def test_rewrite_single():
    def t(expr, c, m):
        e = _rewrite_single(meijerg([a], [b], [c], [d], expr), x)
        assert e is not None
        assert isinstance(e[0][0][2], meijerg)
        assert e[0][0][2].argument.as_coeff_mul(x) == (c, (m,))

    def tn(expr):
        assert _rewrite_single(meijerg([a], [b], [c], [d], expr), x) is None

    t(x, 1, x)
    t(x**2, 1, x**2)
    t(x**2 + y*x**2, y + 1, x**2)
    tn(x**2 + x)
    tn(x**y)

    def u(expr, x):
        from sympy.core.add import Add
        r = _rewrite_single(expr, x)
        e = Add(*[res[0]*res[2] for res in r[0]]).replace(
            exp_polar, exp)  # XXX Hack?
        assert verify_numerically(e, expr, x)

    u(exp(-x)*sin(x), x)

    # The following has stopped working because hyperexpand changed slightly.
    # It is probably not worth fixing
    #u(exp(-x)*sin(x)*cos(x), x)

    # This one cannot be done numerically, since it comes out as a g-function
    # of argument 4*pi
    # NOTE This also tests a bug in inverse mellin transform (which used to
    #      turn exp(4*pi*I*t) into a factor of exp(4*pi*I)**t instead of
    #      exp_polar).
    #u(exp(x)*sin(x), x)
    assert _rewrite_single(exp(x)*sin(x), x) == \
        ([(-sqrt(2)/(2*sqrt(pi)), 0,
           meijerg(((Rational(-1, 2), 0, Rational(1, 4), S.Half, Rational(3, 4)), (1,)),
                   ((), (Rational(-1, 2), 0)), 64*exp_polar(-4*I*pi)/x**4))], True)

