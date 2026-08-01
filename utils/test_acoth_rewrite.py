
def test_acoth_rewrite():
    x = Symbol('x')
    assert acoth(x).rewrite(log) == (log(1 + 1/x) - log(1 - 1/x)) / 2
    assert acoth(x).rewrite(atanh) == atanh(1/x)
    assert acoth(x).rewrite(asinh) == \
        x*sqrt(x**(-2))*asinh(sqrt(1/(x**2 - 1))) + I*pi*(sqrt((x - 1)/x)*sqrt(x/(x - 1)) - sqrt(x/(x + 1))*sqrt(1 + 1/x))/2

