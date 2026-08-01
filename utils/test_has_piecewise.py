
def test_has_piecewise():
    f = (x*y + 3/y)**(3 + 2)
    p = Piecewise((g(x), x < -1), (1, x <= 1), (f, True))

    assert p.has(x)
    assert p.has(y)
    assert not p.has(z)
    assert p.has(1)
    assert p.has(3)
    assert not p.has(4)
    assert p.has(f)
    assert p.has(g)
    assert not p.has(h)

