import re

def test_f_expand_complex():
    x = Symbol('x', real=True)

    assert f(x).expand(complex=True) == I*im(f(x)) + re(f(x))
    assert exp(x).expand(complex=True) == exp(x)
    assert exp(I*x).expand(complex=True) == cos(x) + I*sin(x)
    assert exp(z).expand(complex=True) == cos(im(z))*exp(re(z)) + \
        I*sin(im(z))*exp(re(z))

