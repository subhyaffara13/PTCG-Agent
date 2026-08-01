
def test_PolyElement_gcdex():
    _, x = ring("x", QQ)

    f, g = 2*x, x**2 - 16
    s, t, h = x/32, -QQ(1, 16), 1

    assert f.half_gcdex(g) == (s, h)
    assert f.gcdex(g) == (s, t, h)

