
def test_FracField___hash__():
    F, x, y, z = field("x,y,z", QQ)
    assert hash(F)

