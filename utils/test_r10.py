
def test_R10():
    n, m, r, k = symbols('n m r k', integer=True, positive=True)
    Sm = Sum(binomial(n, k)*binomial(m, r - k), (k, 0, r))
    T = Sm.doit()
    T2 = T.combsimp().rewrite(factorial)
    assert T2 == factorial(m + n)/(factorial(r)*factorial(m + n - r))
    assert T2 == binomial(m + n, r).rewrite(factorial)
    # rewrite(binomial) is not working.
    # https://github.com/sympy/sympy/issues/7135
    T3 = T2.rewrite(binomial)
    assert T3 == binomial(m + n, r)

