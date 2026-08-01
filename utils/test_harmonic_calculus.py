
def test_harmonic_calculus():
    y = Symbol("y", positive=True)
    z = Symbol("z", negative=True)
    assert harmonic(x, 1).limit(x, 0) == 0
    assert harmonic(x, y).limit(x, 0) == 0
    assert harmonic(x, 1).series(x, y, 2) == \
            harmonic(y) + (x - y)*zeta(2, y + 1) + O((x - y)**2, (x, y))
    assert limit(harmonic(x, y), x, oo) == harmonic(oo, y)
    assert limit(harmonic(x, y + 1), x, oo) == zeta(y + 1)
    assert limit(harmonic(x, y - 1), x, oo) == harmonic(oo, y - 1)
    assert limit(harmonic(x, z), x, oo) == Limit(harmonic(x, z), x, oo, dir='-')
    assert limit(harmonic(x, z + 1), x, oo) == oo
    assert limit(harmonic(x, z + 2), x, oo) == harmonic(oo, z + 2)
    assert limit(harmonic(x, z - 1), x, oo) == Limit(harmonic(x, z - 1), x, oo, dir='-')

