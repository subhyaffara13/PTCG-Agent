
def test_PolyElement_LC():
    R, x, y = ring("x,y", QQ, lex)
    assert R(0).LC == QQ(0)
    assert (QQ(1,2)*x).LC == QQ(1, 2)
    assert (QQ(1,4)*x*y + QQ(1,2)*x).LC == QQ(1, 4)

