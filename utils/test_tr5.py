
def test_TR5():
    assert TR5(sin(x)**2) == -cos(x)**2 + 1
    assert TR5(sin(x)**-2) == sin(x)**(-2)
    assert TR5(sin(x)**4) == (-cos(x)**2 + 1)**2

