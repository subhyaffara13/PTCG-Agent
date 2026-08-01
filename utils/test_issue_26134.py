
def test_issue_26134():
    x = Symbol('x')
    assert marcumq(2, 3, 4).rewrite(Integral, x=x).dummy_eq(
        Integral(x**2*exp(-x**2/2 - Rational(9, 2))*besseli(1, 3*x), (x, 4, oo))/3)

