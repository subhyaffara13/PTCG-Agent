
def test_puiseux_ring_attributes():
    R1, px1, py1 = ring('x, y', QQ)
    R2, px2, py2 = puiseux_ring('x, y', QQ)
    assert R2.domain == QQ
    assert R2.symbols == (x, y)
    assert R2.gens == (px2, py2)
    assert R2.ngens == 2
    assert R2.poly_ring == R1
    assert R2.zero == PuiseuxPoly(R1.zero, R2)
    assert R2.one == PuiseuxPoly(R1.one, R2)
    assert R2.zero_monom == R1.zero_monom == (0, 0) # type: ignore
    assert R2.monomial_mul((1, 2), (3, 4)) == (4, 6)

