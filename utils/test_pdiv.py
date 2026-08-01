
def test_pdiv():
    f, g = x**2 - y**2, x - y
    q, r = x + y, 0

    F, G, Q, R = [ Poly(h, x, y) for h in (f, g, q, r) ]

    assert F.pdiv(G) == (Q, R)
    assert F.prem(G) == R
    assert F.pquo(G) == Q
    assert F.pexquo(G) == Q

    assert pdiv(f, g) == (q, r)
    assert prem(f, g) == r
    assert pquo(f, g) == q
    assert pexquo(f, g) == q

    assert pdiv(f, g, x, y) == (q, r)
    assert prem(f, g, x, y) == r
    assert pquo(f, g, x, y) == q
    assert pexquo(f, g, x, y) == q

    assert pdiv(f, g, (x, y)) == (q, r)
    assert prem(f, g, (x, y)) == r
    assert pquo(f, g, (x, y)) == q
    assert pexquo(f, g, (x, y)) == q

    assert pdiv(F, G) == (Q, R)
    assert prem(F, G) == R
    assert pquo(F, G) == Q
    assert pexquo(F, G) == Q

    assert pdiv(f, g, polys=True) == (Q, R)
    assert prem(f, g, polys=True) == R
    assert pquo(f, g, polys=True) == Q
    assert pexquo(f, g, polys=True) == Q

    assert pdiv(F, G, polys=False) == (q, r)
    assert prem(F, G, polys=False) == r
    assert pquo(F, G, polys=False) == q
    assert pexquo(F, G, polys=False) == q

    raises(ComputationFailed, lambda: pdiv(4, 2))
    raises(ComputationFailed, lambda: prem(4, 2))
    raises(ComputationFailed, lambda: pquo(4, 2))
    raises(ComputationFailed, lambda: pexquo(4, 2))

