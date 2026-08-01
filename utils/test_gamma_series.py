
def test_gamma_series():
    assert gamma(x + 1).series(x, 0, 3) == \
        1 - EulerGamma*x + x**2*(EulerGamma**2/2 + pi**2/12) + O(x**3)
    assert gamma(x).series(x, -1, 3) == \
        -1/(x + 1) + EulerGamma - 1 + (x + 1)*(-1 - pi**2/12 - EulerGamma**2/2 + \
       EulerGamma) + (x + 1)**2*(-1 - pi**2/12 - EulerGamma**2/2 + EulerGamma**3/6 - \
       polygamma(2, 1)/6 + EulerGamma*pi**2/12 + EulerGamma) + O((x + 1)**3, (x, -1))

