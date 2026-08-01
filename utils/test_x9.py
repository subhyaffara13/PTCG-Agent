
def test_X9():
    assert (series(x**x, x, x0=0, n=4) == 1 + x*log(x) + x**2*log(x)**2/2 +
            x**3*log(x)**3/6 + O(x**4*log(x)**4))

