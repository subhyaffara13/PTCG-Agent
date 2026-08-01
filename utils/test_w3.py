
def test_W3():
    # integral is not  calculated
    # https://github.com/sympy/sympy/issues/7161
    assert integrate(sqrt(x + 1/x - 2), (x, 0, 1)) == R(4, 3)

