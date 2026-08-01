
def test_hermite_prob():
    assert hermite_prob(0, x) == 1
    assert hermite_prob(1, x) == x
    assert hermite_prob(2, x) == x**2 - 1
    assert hermite_prob(3, x) == x**3 - 3*x
    assert hermite_prob(4, x) == x**4 - 6*x**2 + 3
    assert hermite_prob(6, x) == x**6 - 15*x**4 + 45*x**2 - 15

    n = Symbol("n")
    assert unchanged(hermite_prob, n, x)
    assert hermite_prob(n, -x) == (-1)**n*hermite_prob(n, x)
    assert unchanged(hermite_prob, -n, x)

    assert hermite_prob(n, 0) == sqrt(pi)/gamma(S.Half - n/2)
    assert hermite_prob(n, oo) is oo

    assert conjugate(hermite_prob(n, x)) == hermite_prob(n, conjugate(x))

    _k = Dummy('k')
    assert hermite_prob(n, x).rewrite(Sum).dummy_eq(factorial(n) *
        Sum((-S.Half)**_k * x**(n-2*_k) / (factorial(_k) * factorial(n-2*_k)),
        (_k, 0, floor(n/2))))
    assert hermite_prob(n, x).rewrite("polynomial").dummy_eq(factorial(n) *
        Sum((-S.Half)**_k * x**(n-2*_k) / (factorial(_k) * factorial(n-2*_k)),
        (_k, 0, floor(n/2))))

    assert diff(hermite_prob(n, x), x) == n*hermite_prob(n-1, x)
    assert diff(hermite_prob(n, x), n) == Derivative(hermite_prob(n, x), n)
    raises(ArgumentIndexError, lambda: hermite_prob(n, x).fdiff(3))

    assert hermite_prob(n, x).rewrite(hermite) == \
            sqrt(2)**(-n) * hermite(n, x/sqrt(2))

