
def test_PolynomialRing__init():
    R, = ring("", ZZ)
    assert ZZ.poly_ring() == R.to_domain()

