
def test_atanh():
    R, x, y = ring('x, y', QQ)
    assert rs_atanh(x, x, 9) == x + x**3/3 + x**5/5 + x**7/7
    assert rs_atanh(x*y + x**2*y**3, x, 9) == 2*x**8*y**11 + x**8*y**9 + \
        2*x**7*y**9 + x**7*y**7/7 + x**6*y**9/3 + x**6*y**7 + x**5*y**7 + \
        x**5*y**5/5 + x**4*y**5 + x**3*y**3/3 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', EX)
    assert rs_atanh(x + a, x, 5) == EX((a**3 + a)/(a**8 - 4*a**6 + 6*a**4 - \
        4*a**2 + 1))*x**4 - EX((3*a**2 + 1)/(3*a**6 - 9*a**4 + \
        9*a**2 - 3))*x**3 + EX(a/(a**4 - 2*a**2 + 1))*x**2 - EX(1/(a**2 - \
        1))*x + EX(atanh(a))
    assert rs_atanh(x + x**2*y + a, x, 4) == EX(2*a/(a**4 - 2*a**2 + \
        1))*x**3*y - EX((3*a**2 + 1)/(3*a**6 - 9*a**4 + 9*a**2 - 3))*x**3 - \
        EX(1/(a**2 - 1))*x**2*y + EX(a/(a**4 - 2*a**2 + 1))*x**2 - \
        EX(1/(a**2 - 1))*x + EX(atanh(a))

    p = x + x**2 + 5
    assert rs_atanh(p, x, 10).compose(x, 10) == EX(Rational(-733442653682135, 5079158784) \
        + atanh(5))

    # Test for _atanh faster for small and univariate series
    R,x  = ring('x', QQ)
    p = x**2 + 2*x
    assert _atanh(p, x, 5) == rs_atanh(p, x, 5)

    R,x = ring('x', EX)
    p = x**2 + 2*x
    assert _atanh(p, x, 9) == rs_atanh(p, x, 9)


def test_atanh():
    a = atanh(interval(-0.5, 0.5))
    assert a.start == np.arctanh(-0.5)
    assert a.end == np.arctanh(0.5)

    a = atanh(interval(0, 3))
    assert a.is_valid is None

    a = atanh(interval(-3, -2))
    assert a.is_valid is False

    a = atanh(0.5)
    assert a.start == np.arctanh(0.5)
    assert a.end == np.arctanh(0.5)

    a = atanh(1.5)
    assert a.is_valid is False


def test_atanh():
    x = Symbol('x')

    # at specific points
    assert atanh(0) == 0
    assert atanh(I) == I*pi/4
    assert atanh(-I) == -I*pi/4
    assert atanh(1) is oo
    assert atanh(-1) is -oo
    assert atanh(nan) is nan

    # at infinites
    assert atanh(oo) == -I*pi/2
    assert atanh(-oo) == I*pi/2

    assert atanh(I*oo) == I*pi/2
    assert atanh(-I*oo) == -I*pi/2

    assert atanh(zoo) == I*AccumBounds(-pi/2, pi/2)

    # properties
    assert atanh(-x) == -atanh(x)

    # reality
    assert atanh(S(2)).is_real is False
    assert atanh(S(-1)/5).is_real is True
    assert atanh(symbols('y', extended_real=True)).is_real is None
    assert atanh(S(1)).is_real is False
    assert atanh(S(1)).is_extended_real is True
    assert atanh(S(-1)).is_real is False

    # special values
    assert atanh(I/sqrt(3)) == I*pi/6
    assert atanh(-I/sqrt(3)) == -I*pi/6
    assert atanh(I*sqrt(3)) == I*pi/3
    assert atanh(-I*sqrt(3)) == -I*pi/3
    assert atanh(I*(1 + sqrt(2))) == pi*I*Rational(3, 8)
    assert atanh(I*(sqrt(2) - 1)) == pi*I/8
    assert atanh(I*(1 - sqrt(2))) == -pi*I/8
    assert atanh(-I*(1 + sqrt(2))) == pi*I*Rational(-3, 8)
    assert atanh(I*sqrt(5 + 2*sqrt(5))) == I*pi*Rational(2, 5)
    assert atanh(-I*sqrt(5 + 2*sqrt(5))) == I*pi*Rational(-2, 5)
    assert atanh(I*(2 - sqrt(3))) == pi*I/12
    assert atanh(I*(sqrt(3) - 2)) == -pi*I/12
    assert atanh(oo) == -I*pi/2

    # Symmetry
    assert atanh(Rational(-1, 2)) == -atanh(S.Half)

    # inverse composition
    assert unchanged(atanh, tanh(Symbol('v1')))

    assert atanh(tanh(-5, evaluate=False)) == -5
    assert atanh(tanh(0, evaluate=False)) == 0
    assert atanh(tanh(7, evaluate=False)) == 7
    assert atanh(tanh(I, evaluate=False)) == I
    assert atanh(tanh(-I, evaluate=False)) == -I
    assert atanh(tanh(-11*I, evaluate=False)) == -11*I + 4*I*pi
    assert atanh(tanh(3 + I)) == 3 + I
    assert atanh(tanh(4 + 5*I)) == 4 - 2*I*pi + 5*I
    assert atanh(tanh(pi/2)) == pi/2
    assert atanh(tanh(pi)) == pi
    assert atanh(tanh(-3 + 7*I)) == -3 - 2*I*pi + 7*I
    assert atanh(tanh(9 - I*2/3)) == 9 - I*2/3
    assert atanh(tanh(-32 - 123*I)) == -32 - 123*I + 39*I*pi


def test_atanh():
    mp.dps = 15
    assert atanh(0) == 0
    assert atanh(0.5).ae(0.54930614433405484570)
    assert atanh(-0.5).ae(-0.54930614433405484570)
    assert atanh(1) == inf
    assert atanh(-1) == -inf
    assert isnan(atanh(nan))
    assert isinstance(atanh(1), mpf)
    assert isinstance(atanh(-1), mpf)
    # Limits at infinity
    jpi2 = j*pi/2
    assert atanh(inf).ae(-jpi2)
    assert atanh(-inf).ae(jpi2)
    assert atanh(mpc(inf,-1)).ae(-jpi2)
    assert atanh(mpc(inf,0)).ae(-jpi2)
    assert atanh(mpc(inf,1)).ae(jpi2)
    assert atanh(mpc(1,inf)).ae(jpi2)
    assert atanh(mpc(0,inf)).ae(jpi2)
    assert atanh(mpc(-1,inf)).ae(jpi2)
    assert atanh(mpc(-inf,1)).ae(jpi2)
    assert atanh(mpc(-inf,0)).ae(jpi2)
    assert atanh(mpc(-inf,-1)).ae(-jpi2)
    assert atanh(mpc(-1,-inf)).ae(-jpi2)
    assert atanh(mpc(0,-inf)).ae(-jpi2)
    assert atanh(mpc(1,-inf)).ae(-jpi2)

