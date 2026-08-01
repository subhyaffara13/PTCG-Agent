
def test_FracField___eq__():
    assert field("x,y,z", QQ)[0] == field("x,y,z", QQ)[0]
    assert field("x,y,z", QQ)[0] != field("x,y,z", ZZ)[0]
    assert field("x,y,z", ZZ)[0] != field("x,y,z", QQ)[0]
    assert field("x,y,z", QQ)[0] != field("x,y", QQ)[0]
    assert field("x,y", QQ)[0] != field("x,y,z", QQ)[0]

