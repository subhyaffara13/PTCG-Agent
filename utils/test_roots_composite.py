
def test_roots_composite():
    assert len(roots(Poly(y**3 + y**2*sqrt(x) + y + x, y, composite=True))) == 3

