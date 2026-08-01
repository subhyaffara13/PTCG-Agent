
def test_binomial_rewrite():
    n = Symbol('n', integer=True)
    k = Symbol('k', integer=True)
    x = Symbol('x')

    assert binomial(n, k).rewrite(
        factorial) == factorial(n)/(factorial(k)*factorial(n - k))
    assert binomial(
        n, k).rewrite(gamma) == gamma(n + 1)/(gamma(k + 1)*gamma(n - k + 1))
    assert binomial(n, k).rewrite(ff) == ff(n, k) / factorial(k)
    assert binomial(n, x).rewrite(ff) == binomial(n, x)

