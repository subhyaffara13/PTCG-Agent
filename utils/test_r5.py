
def test_R5():
    a, b, c, n, k = symbols('a b c n k', integer=True, positive=True)
    sk = ((-1)**k)*(binomial(a + b, a + k)
                    *binomial(b + c, b + k)*binomial(c + a, c + k))
    Sm = Sum(sk, (k, 1, oo))
    T = Sm.doit()  # hypergeometric series not calculated
    assert T == factorial(a+b+c)/(factorial(a)*factorial(b)*factorial(c))

