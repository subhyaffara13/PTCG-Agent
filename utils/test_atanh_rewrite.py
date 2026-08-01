
def test_atanh_rewrite():
    x = Symbol('x')
    assert atanh(x).rewrite(log) == (log(1 + x) - log(1 - x)) / 2
    assert atanh(x).rewrite(asinh) == \
        pi*x/(2*sqrt(-x**2)) - sqrt(-x)*sqrt(1 - x**2)*sqrt(1/(x**2 - 1))*asinh(sqrt(1/(x**2 - 1)))/sqrt(x)

