
def test_issue_14177():
    n = Symbol('n', nonnegative=True, integer=True)

    assert zeta(-n).rewrite(bernoulli) == bernoulli(n+1) / (-n-1)
    assert zeta(-n, a).rewrite(bernoulli) == bernoulli(n+1, a) / (-n-1)
    z2n = -(2*I*pi)**(2*n)*bernoulli(2*n) / (2*factorial(2*n))
    assert zeta(2*n).rewrite(bernoulli) == z2n
    assert expand_func(zeta(s, n+1)) == zeta(s) - harmonic(n, s)
    assert expand_func(zeta(-b, -n)) is nan
    assert expand_func(zeta(-b, n)) == zeta(-b, n)

    n = Symbol('n')

    assert zeta(2*n) == zeta(2*n) # As sign of z (= 2*n) is not determined

