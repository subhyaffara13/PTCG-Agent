
def test_has_polys():
    poly = Poly(x**2 + x*y*sin(z), x, y, t)

    assert poly.has(x)
    assert poly.has(x, y, z)
    assert poly.has(x, y, z, t)

