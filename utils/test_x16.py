
def test_X16():
    # Multivariate Taylor series expansion => 1 - (x^2 + 2 x y + y^2)/2 + O(x^4)
    assert (series(cos(x + y), x + y, x0=0, n=4) == 1 - (x + y)**2/2 +
            O(x**4 + x**3*y + x**2*y**2 + x*y**3 + y**4, x, y))

