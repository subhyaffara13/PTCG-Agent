
def test_puiseux_poly():
    R1, px1 = ring('x', QQ)
    R2, px2 = puiseux_ring('x', QQ)
    assert PuiseuxPoly(px1, R2) == px2
    assert px2.ring == R2
    assert px2.as_expr() == px1.as_expr() == x
    assert px1 != px2
    assert R2.one == px2**0 == 1
    assert px2 == px1
    assert px2 != 2.0
    assert px2**QQ(1,2) != px1

