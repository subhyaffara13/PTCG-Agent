
def test_PolyElement_factor_list():
    _, x = ring("x", ZZ)

    f = x**5 - x**3 - x**2 + 1

    u = x + 1
    v = x - 1
    w = x**2 + x + 1

    assert f.factor_list() == (1, [(u, 1), (v, 2), (w, 1)])

