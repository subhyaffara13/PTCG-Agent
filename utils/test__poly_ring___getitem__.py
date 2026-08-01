
def test_PolyRing___getitem__():
    R, x,y,z = ring("x,y,z", ZZ)

    assert R[0:] == PolyRing("x,y,z", ZZ, lex)
    assert R[1:] == PolyRing("y,z", ZZ, lex)
    assert R[2:] == PolyRing("z", ZZ, lex)
    assert R[3:] == ZZ

