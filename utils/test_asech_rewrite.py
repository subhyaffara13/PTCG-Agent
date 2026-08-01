
def test_asech_rewrite():
    x = Symbol('x')
    assert asech(x).rewrite(log) == log(1/x + sqrt(1/x - 1) * sqrt(1/x + 1))
    assert asech(x).rewrite(acosh) == acosh(1/x)
    assert asech(x).rewrite(asinh) == sqrt(-1 + 1/x)*(I*asinh(I/x, evaluate=False) + pi/2)/sqrt(1 - 1/x)
    assert asech(x).rewrite(atanh) == \
        sqrt(x + 1)*sqrt(1/(x + 1))*atanh(sqrt(1 - x**2)) + I*pi*(-sqrt(x)*sqrt(1/x) + 1 - I*sqrt(x**2)/(2*sqrt(-x**2)) - I*sqrt(-x)/(2*sqrt(x)))

