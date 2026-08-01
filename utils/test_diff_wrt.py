
def test_diff_wrt():
    class Test(Expr):
        _diff_wrt = True
        is_commutative = True

    t = Test()
    assert integrate(t + 1, t) == t**2/2 + t
    assert integrate(t + 1, (t, 0, 1)) == Rational(3, 2)

    raises(ValueError, lambda: integrate(x + 1, x + 1))
    raises(ValueError, lambda: integrate(x + 1, (x + 1, 0, 1)))


def test_diff_wrt():
    fx = f(x)
    dfx = diff(f(x), x)
    ddfx = diff(f(x), x, x)

    assert diff(sin(fx) + fx**2, fx) == cos(fx) + 2*fx
    assert diff(sin(dfx) + dfx**2, dfx) == cos(dfx) + 2*dfx
    assert diff(sin(ddfx) + ddfx**2, ddfx) == cos(ddfx) + 2*ddfx
    assert diff(fx**2, dfx) == 0
    assert diff(fx**2, ddfx) == 0
    assert diff(dfx**2, fx) == 0
    assert diff(dfx**2, ddfx) == 0
    assert diff(ddfx**2, dfx) == 0

    assert diff(fx*dfx*ddfx, fx) == dfx*ddfx
    assert diff(fx*dfx*ddfx, dfx) == fx*ddfx
    assert diff(fx*dfx*ddfx, ddfx) == fx*dfx

    assert diff(f(x), x).diff(f(x)) == 0
    assert (sin(f(x)) - cos(diff(f(x), x))).diff(f(x)) == cos(f(x))

    assert diff(sin(fx), fx, x) == diff(sin(fx), x, fx)

    # Chain rule cases
    assert f(g(x)).diff(x) == \
        Derivative(g(x), x)*Derivative(f(g(x)), g(x))
    assert diff(f(g(x), h(y)), x) == \
        Derivative(g(x), x)*Derivative(f(g(x), h(y)), g(x))
    assert diff(f(g(x), h(x)), x) == (
        Derivative(f(g(x), h(x)), g(x))*Derivative(g(x), x) +
        Derivative(f(g(x), h(x)), h(x))*Derivative(h(x), x))
    assert f(
        sin(x)).diff(x) == cos(x)*Subs(Derivative(f(x), x), x, sin(x))

    assert diff(f(g(x)), g(x)) == Derivative(f(g(x)), g(x))

