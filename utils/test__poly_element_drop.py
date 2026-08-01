
def test_PolyElement_drop():
    R, x,y,z = ring("x,y,z", ZZ)

    assert R(1).drop(0).ring == PolyRing("y,z", ZZ, lex)
    assert R(1).drop(0).drop(0).ring == PolyRing("z", ZZ, lex)
    assert R.is_element(R(1).drop(0).drop(0).drop(0)) is False

    raises(ValueError, lambda: z.drop(0).drop(0).drop(0))
    raises(ValueError, lambda: x.drop(0))

