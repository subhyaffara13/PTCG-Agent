
def test_S3():
    n, k = symbols('n k', integer=True, positive=True)
    assert Product(x**k, (k, 1, n)).doit().simplify() == x**(n*(n + 1)/2)

