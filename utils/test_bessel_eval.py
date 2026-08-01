
def test_bessel_eval():
    n, m, k = Symbol('n', integer=True), Symbol('m'), Symbol('k', integer=True, zero=False)

    for f in [besselj, besseli]:
        assert f(0, 0) is S.One
        assert f(2.1, 0) is S.Zero
        assert f(-3, 0) is S.Zero
        assert f(-10.2, 0) is S.ComplexInfinity
        assert f(1 + 3*I, 0) is S.Zero
        assert f(-3 + I, 0) is S.ComplexInfinity
        assert f(-2*I, 0) is S.NaN
        assert f(n, 0) != S.One and f(n, 0) != S.Zero
        assert f(m, 0) != S.One and f(m, 0) != S.Zero
        assert f(k, 0) is S.Zero

    assert bessely(0, 0) is S.NegativeInfinity
    assert besselk(0, 0) is S.Infinity
    for f in [bessely, besselk]:
        assert f(1 + I, 0) is S.ComplexInfinity
        assert f(I, 0) is S.NaN

    for f in [besselj, bessely]:
        assert f(m, S.Infinity) is S.Zero
        assert f(m, S.NegativeInfinity) is S.Zero

    for f in [besseli, besselk]:
        assert f(m, I*S.Infinity) is S.Zero
        assert f(m, I*S.NegativeInfinity) is S.Zero

    for f in [besseli, besselk]:
        assert f(-4, z) == f(4, z)
        assert f(-3, z) == f(3, z)
        assert f(-n, z) == f(n, z)
        assert f(-m, z) != f(m, z)

    for f in [besselj, bessely]:
        assert f(-4, z) == f(4, z)
        assert f(-3, z) == -f(3, z)
        assert f(-n, z) == (-1)**n*f(n, z)
        assert f(-m, z) != (-1)**m*f(m, z)

    for f in [besselj, besseli]:
        assert f(m, -z) == (-z)**m*z**(-m)*f(m, z)

    assert besseli(2, -z) == besseli(2, z)
    assert besseli(3, -z) == -besseli(3, z)

    assert besselj(0, -z) == besselj(0, z)
    assert besselj(1, -z) == -besselj(1, z)

    assert besseli(0, I*z) == besselj(0, z)
    assert besseli(1, I*z) == I*besselj(1, z)
    assert besselj(3, I*z) == -I*besseli(3, z)

