
def test_FracElement_copy():
    F, x, y, z = field("x,y,z", ZZ)

    f = x*y/3*z
    g = f.copy()

    assert f == g
    g.numer[(1, 1, 1)] = 7
    assert f != g

