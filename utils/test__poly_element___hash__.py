
def test_PolyElement___hash__():
    R, x, y, z = ring("x,y,z", QQ)
    assert hash(x*y*z)

