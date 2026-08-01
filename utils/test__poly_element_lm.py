
def test_PolyElement_LM():
    R, x, y = ring("x,y", QQ, lex)
    assert R(0).LM == (0, 0)
    assert (QQ(1,2)*x).LM == (1, 0)
    assert (QQ(1,4)*x*y + QQ(1,2)*x).LM == (1, 1)

