
def test_digamma_expand_func():
    assert digamma(x).expand(func=True) == polygamma(0, x)
    assert digamma(2*x).expand(func=True) == \
        polygamma(0, x)/2 + polygamma(0, Rational(1, 2) + x)/2 + log(2)
    assert digamma(-1 + x).expand(func=True) == \
        polygamma(0, x) - 1/(x - 1)
    assert digamma(1 + x).expand(func=True) == \
        1/x + polygamma(0, x )
    assert digamma(2 + x).expand(func=True) == \
        1/x + 1/(1 + x) + polygamma(0, x)
    assert digamma(3 + x).expand(func=True) == \
        polygamma(0, x) + 1/x + 1/(1 + x) + 1/(2 + x)
    assert digamma(4 + x).expand(func=True) == \
        polygamma(0, x) + 1/x + 1/(1 + x) + 1/(2 + x) + 1/(3 + x)
    assert digamma(x + y).expand(func=True) == \
        polygamma(0, x + y)

