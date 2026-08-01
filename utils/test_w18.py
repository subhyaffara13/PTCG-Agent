
def test_W18():
    assert integrate((besselj(1, x)/x)**2, (x, 0, oo)) == 4/(3*pi)

