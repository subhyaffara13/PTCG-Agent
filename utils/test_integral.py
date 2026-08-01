
def test_integral():
    if numpy and not scipy:
        skip("scipy not installed.")
    f = Lambda(x, exp(-x**2))
    l = lambdify(y, Integral(f(x), (x, y, oo)))
    d = l(-oo)
    assert 1.77245385 < d < 1.772453851

