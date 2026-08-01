
def test_X10():
    z, w = symbols('z w')
    assert (series(log(sinh(z)) + log(cosh(z + w)), z, x0=0, n=2) ==
            log(cosh(w)) + log(z) + z*sinh(w)/cosh(w) + O(z**2))

