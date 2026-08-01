
def test_PolyElement_LT():
    R, x, y = ring("x,y", QQ, lex)
    assert R(0).LT == ((0, 0), QQ(0))
    assert (QQ(1,2)*x).LT == ((1, 0), QQ(1, 2))
    assert (QQ(1,4)*x*y + QQ(1,2)*x).LT == ((1, 1), QQ(1, 4))

    R, = ring("", ZZ)
    assert R(0).LT == ((), 0)
    assert R(1).LT == ((), 1)

