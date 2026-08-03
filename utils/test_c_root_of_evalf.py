import re

def test_CRootOf_evalf():
    real = rootof(x**3 + x + 3, 0).evalf(n=20)

    assert real.epsilon_eq(Float("-1.2134116627622296341"))

    re, im = rootof(x**3 + x + 3, 1).evalf(n=20).as_real_imag()

    assert re.epsilon_eq( Float("0.60670583138111481707"))
    assert im.epsilon_eq(-Float("1.45061224918844152650"))

    re, im = rootof(x**3 + x + 3, 2).evalf(n=20).as_real_imag()

    assert re.epsilon_eq(Float("0.60670583138111481707"))
    assert im.epsilon_eq(Float("1.45061224918844152650"))

    p = legendre_poly(4, x, polys=True)
    roots = [str(r.n(17)) for r in p.real_roots()]
    # magnitudes are given by
    # sqrt(3/S(7) - 2*sqrt(6/S(5))/7)
    #   and
    # sqrt(3/S(7) + 2*sqrt(6/S(5))/7)
    assert roots == [
            "-0.86113631159405258",
            "-0.33998104358485626",
             "0.33998104358485626",
             "0.86113631159405258",
             ]

    re = rootof(x**5 - 5*x + 12, 0).evalf(n=20)
    assert re.epsilon_eq(Float("-1.84208596619025438271"))

    re, im = rootof(x**5 - 5*x + 12, 1).evalf(n=20).as_real_imag()
    assert re.epsilon_eq(Float("-0.351854240827371999559"))
    assert im.epsilon_eq(Float("-1.709561043370328882010"))

    re, im = rootof(x**5 - 5*x + 12, 2).evalf(n=20).as_real_imag()
    assert re.epsilon_eq(Float("-0.351854240827371999559"))
    assert im.epsilon_eq(Float("+1.709561043370328882010"))

    re, im = rootof(x**5 - 5*x + 12, 3).evalf(n=20).as_real_imag()
    assert re.epsilon_eq(Float("+1.272897223922499190910"))
    assert im.epsilon_eq(Float("-0.719798681483861386681"))

    re, im = rootof(x**5 - 5*x + 12, 4).evalf(n=20).as_real_imag()
    assert re.epsilon_eq(Float("+1.272897223922499190910"))
    assert im.epsilon_eq(Float("+0.719798681483861386681"))

    # issue 6393
    assert str(rootof(x**5 + 2*x**4 + x**3 - 68719476736, 0).n(3)) == '147.'
    eq = (531441*x**11 + 3857868*x**10 + 13730229*x**9 + 32597882*x**8 +
        55077472*x**7 + 60452000*x**6 + 32172064*x**5 - 4383808*x**4 -
        11942912*x**3 - 1506304*x**2 + 1453312*x + 512)
    a, b = rootof(eq, 1).n(2).as_real_imag()
    c, d = rootof(eq, 2).n(2).as_real_imag()
    assert a == c
    assert b < d
    assert b == -d
    # issue 6451
    r = rootof(legendre_poly(64, x), 7)
    assert r.n(2) == r.n(100).n(2)
    # issue 9019
    r0 = rootof(x**2 + 1, 0, radicals=False)
    r1 = rootof(x**2 + 1, 1, radicals=False)
    assert r0.n(4) == Float(-1.0, 4) * I
    assert r1.n(4) == Float(1.0, 4) * I

    # make sure verification is used in case a max/min traps the "root"
    assert str(rootof(4*x**5 + 16*x**3 + 12*x**2 + 7, 0).n(3)) == '-0.976'

    # watch out for UnboundLocalError
    c = CRootOf(90720*x**6 - 4032*x**4 + 84*x**2 - 1, 0)
    assert c._eval_evalf(2)  # doesn't fail

    # watch out for imaginary parts that don't want to evaluate
    assert str(RootOf(x**16 + 32*x**14 + 508*x**12 + 5440*x**10 +
        39510*x**8 + 204320*x**6 + 755548*x**4 + 1434496*x**2 +
        877969, 10).n(2)) == '-3.4*I'
    assert abs(RootOf(x**4 + 10*x**2 + 1, 0).n(2)) < 0.4

    # check reset and args
    r = [RootOf(x**3 + x + 3, i) for i in range(3)]
    r[0]._reset()
    for ri in r:
        i = ri._get_interval()
        ri.n(2)
        assert i != ri._get_interval()
        ri._reset()
        assert i == ri._get_interval()
        assert i == i.func(*i.args)

