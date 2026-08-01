
def test_W16():
    assert integrate((1 + x)**3*legendre_poly(1, x)*legendre_poly(2, x),
                     (x, -1, 1)) == R(36, 35)

