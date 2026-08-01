
def test_xtothex():
    a = risch_integrate(x**x, x)
    assert a == NonElementaryIntegral(x**x, x)
    assert isinstance(a, NonElementaryIntegral)

