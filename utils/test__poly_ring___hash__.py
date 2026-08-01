
def test_PolyRing___hash__():
    R, x, y, z = ring("x,y,z", QQ)
    assert hash(R)

