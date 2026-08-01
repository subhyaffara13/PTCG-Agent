
def test_meijerg_eval():
    from sympy.functions.elementary.exponential import exp_polar
    from sympy.functions.special.bessel import besseli
    from sympy.abc import l
    a = randcplx()
    arg = x*exp_polar(k*pi*I)
    expr1 = pi*meijerg([[], [(a + 1)/2]], [[a/2], [-a/2, (a + 1)/2]], arg**2/4)
    expr2 = besseli(a, arg)

    # Test that the two expressions agree for all arguments.
    for x_ in [0.5, 1.5]:
        for k_ in [0.0, 0.1, 0.3, 0.5, 0.8, 1, 5.751, 15.3]:
            assert abs((expr1 - expr2).n(subs={x: x_, k: k_})) < 1e-10
            assert abs((expr1 - expr2).n(subs={x: x_, k: -k_})) < 1e-10

    # Test continuity independently
    eps = 1e-13
    expr2 = expr1.subs(k, l)
    for x_ in [0.5, 1.5]:
        for k_ in [0.5, Rational(1, 3), 0.25, 0.75, Rational(2, 3), 1.0, 1.5]:
            assert abs((expr1 - expr2).n(
                       subs={x: x_, k: k_ + eps, l: k_ - eps})) < 1e-10
            assert abs((expr1 - expr2).n(
                       subs={x: x_, k: -k_ + eps, l: -k_ - eps})) < 1e-10

    expr = (meijerg(((0.5,), ()), ((0.5, 0, 0.5), ()), exp_polar(-I*pi)/4)
            + meijerg(((0.5,), ()), ((0.5, 0, 0.5), ()), exp_polar(I*pi)/4)) \
        /(2*sqrt(pi))
    assert (expr - pi/exp(1)).n(chop=True) == 0

