
def test_S6():
    n, k = symbols('n k', integer=True, positive=True)
    # Product does not evaluate
    assert (Product(x**2 -2*x*cos(k*pi/n) + 1, (k, 1, n - 1)).doit().simplify()
            == (x**(2*n) - 1)/(x**2 - 1))

