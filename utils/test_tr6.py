
def test_TR6():
    assert TR6(cos(x)**2) == -sin(x)**2 + 1
    assert TR6(cos(x)**-2) == cos(x)**(-2)
    assert TR6(cos(x)**4) == (-sin(x)**2 + 1)**2

