
def test_pmint_trig():
    f = (x - tan(x)) / tan(x)**2 + tan(x)
    g = -x**2/2 - x/tan(x) + log(tan(x)**2 + 1)/2

    assert heurisch(f, x) == g

