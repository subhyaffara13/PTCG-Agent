
def test_puiseux_ring_methods():
    R1, px1, py1 = ring('x, y', QQ)
    R2, px2, py2 = puiseux_ring('x, y', QQ)
    assert R2({(1, 2): 3}) == 3*px2*py2**2
    assert R2(px1) == px2
    assert R2(1) == R2.one
    assert R2(QQ(1,2)) == QQ(1,2)*R2.one
    assert R2.from_poly(px1) == px2
    assert R2.from_poly(px1) != py2
    assert R2.from_dict({(1, 2): QQ(3)}) == 3*px2*py2**2
    assert R2.from_dict({(QQ(1,2), 2): QQ(3)}) == 3*px2**QQ(1,2)*py2**2
    assert R2.from_int(3) == 3*R2.one
    assert R2.domain_new(3) == QQ(3)
    assert QQ.of_type(R2.domain_new(3))
    assert R2.ground_new(3) == 3*R2.one
    assert isinstance(R2.ground_new(3), PuiseuxPoly)
    assert R2.index(px2) == 0
    assert R2.index(py2) == 1

