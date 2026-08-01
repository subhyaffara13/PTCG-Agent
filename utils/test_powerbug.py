
def test_powerbug():
    x = Symbol("x")
    assert x**1 != (-x)**1
    assert x**2 == (-x)**2
    assert x**3 != (-x)**3
    assert x**4 == (-x)**4
    assert x**5 != (-x)**5
    assert x**6 == (-x)**6

    assert x**128 == (-x)**128
    assert x**129 != (-x)**129

    assert (2*x)**2 == (-2*x)**2

