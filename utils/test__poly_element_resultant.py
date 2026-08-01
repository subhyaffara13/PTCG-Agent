
def test_PolyElement_resultant():
    _, x = ring("x", ZZ)
    f, g, h = x**2 - 2*x + 1, x**2 - 1, 0

    assert f.resultant(g) == h

