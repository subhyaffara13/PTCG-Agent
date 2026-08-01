
def test_puiseux_poly_monoms():
    R, x = puiseux_ring('x', QQ)
    assert x.monoms() == [(1,)]
    assert list(x) == [(1,)]
    assert (x**2 + 1).monoms() == [(2,), (0,)]
    assert R({(1,): 1, (-1,): 1}).monoms() == [(1,), (-1,)]
    assert R({(QQ(1,3),): 1}).monoms() == [(QQ(1,3),)]
    assert R({(-QQ(1,3),): 1}).monoms() == [(-QQ(1,3),)]
    p = x**QQ(1,6)
    assert p[(QQ(1,6),)] == 1
    raises(KeyError, lambda: p[(1,)])
    assert p.to_dict() == {(QQ(1,6),): 1}
    assert R(p.to_dict()) == p
    assert PuiseuxPoly.from_dict({(QQ(1,6),): 1}, R) == p

