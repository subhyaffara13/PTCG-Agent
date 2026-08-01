
def test_PolyRing_symmetric_poly():
    R, x, y, z, t = ring("x,y,z,t", ZZ)

    raises(ValueError, lambda: R.symmetric_poly(-1))
    raises(ValueError, lambda: R.symmetric_poly(5))

    assert R.symmetric_poly(0) == R.one
    assert R.symmetric_poly(1) == x + y + z + t
    assert R.symmetric_poly(2) == x*y + x*z + x*t + y*z + y*t + z*t
    assert R.symmetric_poly(3) == x*y*z + x*y*t + x*z*t + y*z*t
    assert R.symmetric_poly(4) == x*y*z*t

