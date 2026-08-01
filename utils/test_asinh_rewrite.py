
def test_asinh_rewrite():
    x = Symbol('x')
    assert asinh(x).rewrite(log) == log(x + sqrt(x**2 + 1))
    assert asinh(x).rewrite(atanh) == atanh(x/sqrt(1 + x**2))
    assert asinh(x).rewrite(asin) == -I*asin(I*x, evaluate=False)
    assert asinh(x*(1 + I)).rewrite(asin) == -I*asin(I*x*(1+I))
    assert asinh(x).rewrite(acos) == I*acos(I*x, evaluate=False) - I*pi/2

