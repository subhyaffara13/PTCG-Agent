
def test_PolyElement_copy():
    R, x, y, z = ring("x,y,z", ZZ)

    f = x*y + 3*z
    g = f.copy()

    assert f == g
    g[(1, 1, 1)] = 7
    assert f != g

