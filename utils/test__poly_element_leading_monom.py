
def test_PolyElement_leading_monom():
    R, x, y = ring("x,y", QQ, lex)
    assert R(0).leading_monom() == 0
    assert (QQ(1,2)*x).leading_monom() == x
    assert (QQ(1,4)*x*y + QQ(1,2)*x).leading_monom() == x*y

