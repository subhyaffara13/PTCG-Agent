
def test_acosh_rewrite():
    x = Symbol('x')
    assert acosh(x).rewrite(log) == log(x + sqrt(x - 1)*sqrt(x + 1))
    assert acosh(x).rewrite(asin) == sqrt(x - 1)*(-asin(x) + pi/2)/sqrt(1 - x)
    assert acosh(x).rewrite(asinh) == sqrt(x - 1)*(I*asinh(I*x, evaluate=False) + pi/2)/sqrt(1 - x)
    assert acosh(x).rewrite(atanh) == \
        (sqrt(x - 1)*sqrt(x + 1)*atanh(sqrt(x**2 - 1)/x)/sqrt(x**2 - 1) +
         pi*sqrt(x - 1)*(-x*sqrt(x**(-2)) + 1)/(2*sqrt(1 - x)))
    x = Symbol('x', positive=True)
    assert acosh(x).rewrite(atanh) == \
        sqrt(x - 1)*sqrt(x + 1)*atanh(sqrt(x**2 - 1)/x)/sqrt(x**2 - 1)

