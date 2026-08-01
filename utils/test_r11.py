
def test_R11():
    n, k = symbols('n k', integer=True, positive=True)
    sk = binomial(n, k)*fibonacci(k)
    Sm = Sum(sk, (k, 0, n))
    T = Sm.doit()
    # Fibonacci simplification not implemented
    # https://github.com/sympy/sympy/issues/7134
    assert T == fibonacci(2*n)

