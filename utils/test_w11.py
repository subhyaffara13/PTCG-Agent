
def test_W11():
    # integral not calculated
    assert (integrate(sqrt(1 - x**2)/(1 + x**2), (x, -1, 1)) ==
            pi*(-1 + sqrt(2)))

