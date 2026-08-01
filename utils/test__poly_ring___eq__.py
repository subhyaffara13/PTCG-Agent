
def test_PolyRing___eq__():
    assert ring("x,y,z", QQ)[0] == ring("x,y,z", QQ)[0]
    assert ring("x,y,z", QQ)[0] != ring("x,y,z", ZZ)[0]
    assert ring("x,y,z", ZZ)[0] != ring("x,y,z", QQ)[0]
    assert ring("x,y,z", QQ)[0] != ring("x,y", QQ)[0]
    assert ring("x,y", QQ)[0] != ring("x,y,z", QQ)[0]

