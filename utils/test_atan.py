import math


def test_atan():
    x = Symbol("x", real=True)
    assert limit(atan(x)*sin(1/x), x, 0) == 0
    assert limit(atan(x) + sqrt(x + 1) - sqrt(x), x, oo) == pi/2


def test_atan():
    R, x, y = ring('x, y', QQ)
    assert rs_atan(x, x, 9) == -x**7/7 + x**5/5 - x**3/3 + x
    assert rs_atan(x*y + x**2*y**3, x, 9) == 2*x**8*y**11 - x**8*y**9 + \
        2*x**7*y**9 - x**7*y**7/7 - x**6*y**9/3 + x**6*y**7 - x**5*y**7 + \
        x**5*y**5/5 - x**4*y**5 - x**3*y**3/3 + x**2*y**3 + x*y

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', EX)
    assert rs_atan(x + a, x, 5) == -EX((a**3 - a)/(a**8 + 4*a**6 + 6*a**4 + \
        4*a**2 + 1))*x**4 + EX((3*a**2 - 1)/(3*a**6 + 9*a**4 + \
        9*a**2 + 3))*x**3 - EX(a/(a**4 + 2*a**2 + 1))*x**2 + \
        EX(1/(a**2 + 1))*x + EX(atan(a))
    assert rs_atan(x + x**2*y + a, x, 4) == -EX(2*a/(a**4 + 2*a**2 + 1)) \
        *x**3*y + EX((3*a**2 - 1)/(3*a**6 + 9*a**4 + 9*a**2 + 3))*x**3 + \
        EX(1/(a**2 + 1))*x**2*y - EX(a/(a**4 + 2*a**2 + 1))*x**2 + EX(1/(a**2 \
        + 1))*x + EX(atan(a))

    # Test for _atan faster for small and univariate series
    R, x = ring('x', QQ)
    p = x**2 + 2*x
    assert _atan(p, x, 5) == rs_atan(p, x, 5)

    R, x = ring('x', EX)
    p = x**2 + 2*x
    assert _atan(p, x, 9) == rs_atan(p, x, 9)


def test_atan():
    a = atan(interval(0, 1))
    assert a.start == np.arctan(0)
    assert a.end == np.arctan(1)
    a = atan(1)
    assert a.start == np.arctan(1)
    assert a.end == np.arctan(1)


def test_atan():
    assert atan(nan) is nan

    assert atan.nargs == FiniteSet(1)
    assert atan(oo) == pi/2
    assert atan(-oo) == -pi/2
    assert atan(zoo) == AccumBounds(-pi/2, pi/2)

    assert atan(0) == 0
    assert atan(1) == pi/4
    assert atan(sqrt(3)) == pi/3
    assert atan(-(1 + sqrt(2))) == pi*Rational(-3, 8)
    assert atan(sqrt(5 - 2 * sqrt(5))) == pi/5
    assert atan(-sqrt(1 - 2 * sqrt(5)/ 5)) == -pi/10
    assert atan(sqrt(1 + 2 * sqrt(5) / 5)) == pi*Rational(3, 10)
    assert atan(-2 + sqrt(3)) == -pi/12
    assert atan(2 + sqrt(3)) == pi*Rational(5, 12)
    assert atan(-2 - sqrt(3)) == pi*Rational(-5, 12)

    # check round-trip for exact values:
    for d in [5, 6, 8, 10, 12]:
        for num in range(-(d//2), d//2 + 1):
            if gcd(num, d) == 1:
                assert atan(tan(num*pi/d)) == num*pi/d

    assert atan(oo) == pi/2
    assert atan(x).diff(x) == 1/(1 + x**2)

    assert atan(r).is_real is True

    assert atan(-2*I) == -I*atanh(2)
    assert unchanged(atan, cot(x))
    assert atan(cot(Rational(1, 4))) == Rational(-1, 4) + pi/2
    assert acot(Rational(1, 4)).is_rational is False

    for s in (x, p, n, np, nn, nz, ep, en, enp, enn, enz):
        if s.is_real or s.is_extended_real is None:
            assert s.is_nonzero is atan(s).is_nonzero
            assert s.is_positive is atan(s).is_positive
            assert s.is_negative is atan(s).is_negative
            assert s.is_nonpositive is atan(s).is_nonpositive
            assert s.is_nonnegative is atan(s).is_nonnegative
        else:
            assert s.is_extended_nonzero is atan(s).is_nonzero
            assert s.is_extended_positive is atan(s).is_positive
            assert s.is_extended_negative is atan(s).is_negative
            assert s.is_extended_nonpositive is atan(s).is_nonpositive
            assert s.is_extended_nonnegative is atan(s).is_nonnegative
        assert s.is_extended_nonzero is atan(s).is_extended_nonzero
        assert s.is_extended_positive is atan(s).is_extended_positive
        assert s.is_extended_negative is atan(s).is_extended_negative
        assert s.is_extended_nonpositive is atan(s).is_extended_nonpositive
        assert s.is_extended_nonnegative is atan(s).is_extended_nonnegative


def test_atan():
    mp.dps = 15
    assert atan(-2.3).ae(math.atan(-2.3))
    assert atan(1e-50) == 1e-50
    assert atan(1e50).ae(pi/2)
    assert atan(-1e-50) == -1e-50
    assert atan(-1e50).ae(-pi/2)
    assert atan(10**1000).ae(pi/2)
    for dps in [25, 70, 100, 300, 1000]:
        mp.dps = dps
        assert (4*atan(1)).ae(pi)
    mp.dps = 15
    pi2 = pi/2
    assert atan(mpc(inf,-1)).ae(pi2)
    assert atan(mpc(inf,0)).ae(pi2)
    assert atan(mpc(inf,1)).ae(pi2)
    assert atan(mpc(1,inf)).ae(pi2)
    assert atan(mpc(0,inf)).ae(pi2)
    assert atan(mpc(-1,inf)).ae(-pi2)
    assert atan(mpc(-inf,1)).ae(-pi2)
    assert atan(mpc(-inf,0)).ae(-pi2)
    assert atan(mpc(-inf,-1)).ae(-pi2)
    assert atan(mpc(-1,-inf)).ae(-pi2)
    assert atan(mpc(0,-inf)).ae(-pi2)
    assert atan(mpc(1,-inf)).ae(pi2)

