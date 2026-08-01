
def test_PolyElement_leading_term():
    R, x, y = ring("x,y", QQ, lex)
    assert R(0).leading_term() == 0
    assert (QQ(1,2)*x).leading_term() == QQ(1,2)*x
    assert (QQ(1,4)*x*y + QQ(1,2)*x).leading_term() == QQ(1,4)*x*y

