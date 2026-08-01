
def test_rewrite():
    assert besselj(n, z).rewrite(jn) == sqrt(2*z/pi)*jn(n - S.Half, z)
    assert bessely(n, z).rewrite(yn) == sqrt(2*z/pi)*yn(n - S.Half, z)
    assert besseli(n, z).rewrite(besselj) == \
        exp(-I*n*pi/2)*besselj(n, polar_lift(I)*z)
    assert besselj(n, z).rewrite(besseli) == \
        exp(I*n*pi/2)*besseli(n, polar_lift(-I)*z)

    nu = randcplx()

    assert tn(besselj(nu, z), besselj(nu, z).rewrite(besseli), z)
    assert tn(besselj(nu, z), besselj(nu, z).rewrite(bessely), z)

    assert tn(besseli(nu, z), besseli(nu, z).rewrite(besselj), z)
    assert tn(besseli(nu, z), besseli(nu, z).rewrite(bessely), z)

    assert tn(bessely(nu, z), bessely(nu, z).rewrite(besselj), z)
    assert tn(bessely(nu, z), bessely(nu, z).rewrite(besseli), z)

    assert tn(besselk(nu, z), besselk(nu, z).rewrite(besselj), z)
    assert tn(besselk(nu, z), besselk(nu, z).rewrite(besseli), z)
    assert tn(besselk(nu, z), besselk(nu, z).rewrite(bessely), z)

    # check that a rewrite was triggered, when the order is set to a generic
    # symbol 'nu'
    assert yn(nu, z) != yn(nu, z).rewrite(jn)
    assert hn1(nu, z) != hn1(nu, z).rewrite(jn)
    assert hn2(nu, z) != hn2(nu, z).rewrite(jn)
    assert jn(nu, z) != jn(nu, z).rewrite(yn)
    assert hn1(nu, z) != hn1(nu, z).rewrite(yn)
    assert hn2(nu, z) != hn2(nu, z).rewrite(yn)

    # rewriting spherical bessel functions (SBFs) w.r.t. besselj, bessely is
    # not allowed if a generic symbol 'nu' is used as the order of the SBFs
    # to avoid inconsistencies (the order of bessel[jy] is allowed to be
    # complex-valued, whereas SBFs are defined only for integer orders)
    order = nu
    for f in (besselj, bessely):
        assert hn1(order, z) == hn1(order, z).rewrite(f)
        assert hn2(order, z) == hn2(order, z).rewrite(f)

    assert jn(order, z).rewrite(besselj) == sqrt(2)*sqrt(pi)*sqrt(1/z)*besselj(order + S.Half, z)/2
    assert jn(order, z).rewrite(bessely) == (-1)**nu*sqrt(2)*sqrt(pi)*sqrt(1/z)*bessely(-order - S.Half, z)/2

    # for integral orders rewriting SBFs w.r.t bessel[jy] is allowed
    N = Symbol('n', integer=True)
    ri = randint(-11, 10)
    for order in (ri, N):
        for f in (besselj, bessely):
            assert yn(order, z) != yn(order, z).rewrite(f)
            assert jn(order, z) != jn(order, z).rewrite(f)
            assert hn1(order, z) != hn1(order, z).rewrite(f)
            assert hn2(order, z) != hn2(order, z).rewrite(f)

    for func, refunc in product((yn, jn, hn1, hn2),
                                (jn, yn, besselj, bessely)):
        assert tn(func(ri, z), func(ri, z).rewrite(refunc), z)


def test_rewrite():
    x, y = Symbol('x', real=True), Symbol('y')
    assert Heaviside(x).rewrite(Piecewise) == (
        Piecewise((0, x < 0), (Heaviside(0), Eq(x, 0)), (1, True)))
    assert Heaviside(y).rewrite(Piecewise) == (
        Piecewise((0, y < 0), (Heaviside(0), Eq(y, 0)), (1, True)))
    assert Heaviside(x, y).rewrite(Piecewise) == (
        Piecewise((0, x < 0), (y, Eq(x, 0)), (1, True)))
    assert Heaviside(x, 0).rewrite(Piecewise) == (
        Piecewise((0, x <= 0), (1, True)))
    assert Heaviside(x, 1).rewrite(Piecewise) == (
        Piecewise((0, x < 0), (1, True)))
    assert Heaviside(x, nan).rewrite(Piecewise) == (
        Piecewise((0, x < 0), (nan, Eq(x, 0)), (1, True)))

    assert Heaviside(x).rewrite(sign) == \
        Heaviside(x, H0=Heaviside(0)).rewrite(sign) == \
        Piecewise(
            (sign(x)/2 + S(1)/2, Eq(Heaviside(0), S(1)/2)),
            (Piecewise(
                (sign(x)/2 + S(1)/2, Ne(x, 0)), (Heaviside(0), True)), True)
        )

    assert Heaviside(y).rewrite(sign) == Heaviside(y)
    assert Heaviside(x, S.Half).rewrite(sign) == (sign(x)+1)/2
    assert Heaviside(x, y).rewrite(sign) == \
        Piecewise(
            (sign(x)/2 + S(1)/2, Eq(y, S(1)/2)),
            (Piecewise(
                (sign(x)/2 + S(1)/2, Ne(x, 0)), (y, True)), True)
        )

    assert DiracDelta(y).rewrite(Piecewise) == Piecewise((DiracDelta(0), Eq(y, 0)), (0, True))
    assert DiracDelta(y, 1).rewrite(Piecewise) == DiracDelta(y, 1)
    assert DiracDelta(x - 5).rewrite(Piecewise) == (
        Piecewise((DiracDelta(0), Eq(x - 5, 0)), (0, True)))

    assert (x*DiracDelta(x - 10)).rewrite(SingularityFunction) == x*SingularityFunction(x, 10, -1)
    assert 5*x*y*DiracDelta(y, 1).rewrite(SingularityFunction) == 5*x*y*SingularityFunction(y, 0, -2)
    assert DiracDelta(0).rewrite(SingularityFunction) == SingularityFunction(0, 0, -1)
    assert DiracDelta(0, 1).rewrite(SingularityFunction) == SingularityFunction(0, 0, -2)

    assert Heaviside(x).rewrite(SingularityFunction) == SingularityFunction(x, 0, 0)
    assert 5*x*y*Heaviside(y + 1).rewrite(SingularityFunction) == 5*x*y*SingularityFunction(y, -1, 0)
    assert ((x - 3)**3*Heaviside(x - 3)).rewrite(SingularityFunction) == (x - 3)**3*SingularityFunction(x, 3, 0)
    assert Heaviside(0).rewrite(SingularityFunction) == S.Half


def test_rewrite():
    assert SingularityFunction(x, 4, 5).rewrite(Piecewise) == (
        Piecewise(((x - 4)**5, x - 4 >= 0), (0, True)))
    assert SingularityFunction(x, -10, 0).rewrite(Piecewise) == (
        Piecewise((1, x + 10 >= 0), (0, True)))
    assert SingularityFunction(x, 2, -1).rewrite(Piecewise) == (
        Piecewise((oo, Eq(x - 2, 0)), (0, True)))
    assert SingularityFunction(x, 0, -2).rewrite(Piecewise) == (
        Piecewise((oo, Eq(x, 0)), (0, True)))

    n = Symbol('n', nonnegative=True)
    p = SingularityFunction(x, a, n).rewrite(Piecewise)
    assert p == (
        Piecewise(((x - a)**n, x - a >= 0), (0, True)))
    assert p.subs(x, a).subs(n, 0) == 1

    expr_in = SingularityFunction(x, 4, 5) + SingularityFunction(x, -3, -1) - SingularityFunction(x, 0, -2)
    expr_out = (x - 4)**5*Heaviside(x - 4, 1) + DiracDelta(x + 3) - DiracDelta(x, 1)
    assert expr_in.rewrite(Heaviside) == expr_out
    assert expr_in.rewrite(DiracDelta) == expr_out
    assert expr_in.rewrite('HeavisideDiracDelta') == expr_out

    expr_in = SingularityFunction(x, a, n) + SingularityFunction(x, a, -1) - SingularityFunction(x, a, -2)
    expr_out = (x - a)**n*Heaviside(x - a, 1) + DiracDelta(x - a) + DiracDelta(a - x, 1)
    assert expr_in.rewrite(Heaviside) == expr_out
    assert expr_in.rewrite(DiracDelta) == expr_out
    assert expr_in.rewrite('HeavisideDiracDelta') == expr_out


def test_rewrite():
    x, y, z = symbols('x y z')
    a, b = symbols('a b')
    f1 = sin(x) + cos(x)
    assert f1.rewrite(cos,exp) == exp(I*x)/2 + sin(x) + exp(-I*x)/2
    assert f1.rewrite([cos],sin) == sin(x) + sin(x + pi/2, evaluate=False)
    f2 = sin(x) + cos(y)/gamma(z)
    assert f2.rewrite(sin,exp) == -I*(exp(I*x) - exp(-I*x))/2 + cos(y)/gamma(z)

    assert f1.rewrite() == f1

