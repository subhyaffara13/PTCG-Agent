
def test_trigamma_expand_func():
    assert trigamma(2*x).expand(func=True) == \
        polygamma(1, x)/4 + polygamma(1, Rational(1, 2) + x)/4
    assert trigamma(1 + x).expand(func=True) == \
        polygamma(1, x) - 1/x**2
    assert trigamma(2 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2
    assert trigamma(3 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2 - 1/(2 + x)**2
    assert trigamma(4 + x).expand(func=True, multinomial=False) == \
        polygamma(1, x) - 1/x**2 - 1/(1 + x)**2 - \
        1/(2 + x)**2 - 1/(3 + x)**2
    assert trigamma(x + y).expand(func=True) == \
        polygamma(1, x + y)
    assert trigamma(3 + 4*x + y).expand(func=True, multinomial=False) == \
        polygamma(1, y + 4*x) - 1/(y + 4*x)**2 - \
        1/(1 + y + 4*x)**2 - 1/(2 + y + 4*x)**2

