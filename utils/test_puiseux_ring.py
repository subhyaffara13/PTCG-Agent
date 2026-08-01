
def test_puiseux_ring():
    R, px = puiseux_ring('x', QQ)
    R2, px2 = puiseux_ring([x], QQ)
    assert isinstance(R, PuiseuxRing)
    assert isinstance(px, PuiseuxPoly)
    assert R == R2
    assert px == px2
    assert R == PuiseuxRing('x', QQ)
    assert R == PuiseuxRing([x], QQ)
    assert R != PuiseuxRing('y', QQ)
    assert R != PuiseuxRing('x', ZZ)
    assert R != PuiseuxRing('x, y', QQ)
    assert R != QQ
    assert str(R) == 'PuiseuxRing((x,), QQ)'

