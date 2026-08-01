
def test_FracElement___hash__():
    F, x, y, z = field("x,y,z", QQ)
    assert hash(x*y/z)

