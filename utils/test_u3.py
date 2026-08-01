
def test_U3():
    f = Lambda(x, Piecewise((x**2 - 1, x == 1), (x**3, x != 1)))
    f1 = Lambda(x, diff(f(x), x))
    assert f1(x) == 3*x**2
    assert f1(1) == 3

