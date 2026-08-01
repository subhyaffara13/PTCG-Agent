
def test_S5():
    n, k = symbols('n k', integer=True, positive=True)
    assert (Product((2*k - 1)/(2*k), (k, 1, n)).doit().gammasimp() ==
            gamma(n + S.Half)/(sqrt(pi)*gamma(n + 1)))

