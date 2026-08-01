
def test_issue_23942():
    I1 = Integral(1/sqrt(a*(1 + x)**3 + (1 + x)**2), (x, 0, z))
    assert I1.series(a, 1, n=1) == Integral(1/sqrt(x**3 + 4*x**2 + 5*x + 2), (x, 0, z)) + O(a - 1, (a, 1))
    I2 = Integral(1/sqrt(a*(4 - x)**4 + (5 + x)**2), (x, 0, z))
    assert I2.series(a, 2, n=1) == Integral(1/sqrt(2*x**4 - 32*x**3 + 193*x**2 - 502*x + 537), (x, 0, z)) + O(a - 2, (a, 2))

