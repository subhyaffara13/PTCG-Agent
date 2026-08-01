
def test_T8():
    a, z = symbols('a z', positive=True)
    assert limit(gamma(z + a)/gamma(z)*exp(-a*log(z)), z, oo) == 1

