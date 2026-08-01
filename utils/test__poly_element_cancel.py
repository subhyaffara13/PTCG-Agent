
def test_PolyElement_cancel():
    R, x, y = ring("x,y", ZZ)

    f = 2*x**3 + 4*x**2 + 2*x
    g = 3*x**2 + 3*x
    F = 2*x + 2
    G = 3

    assert f.cancel(g) == (F, G)

    assert (-f).cancel(g) == (-F, G)
    assert f.cancel(-g) == (-F, G)

    R, x, y = ring("x,y", QQ)

    f = QQ(1,2)*x**3 + x**2 + QQ(1,2)*x
    g = QQ(1,3)*x**2 + QQ(1,3)*x
    F = 3*x + 3
    G = 2

    assert f.cancel(g) == (F, G)

    assert (-f).cancel(g) == (-F, G)
    assert f.cancel(-g) == (-F, G)

    Fx, x = field("x", ZZ)
    Rt, t = ring("t", Fx)

    f = (-x**2 - 4)/4*t
    g = t**2 + (x**2 + 2)/2

    assert f.cancel(g) == ((-x**2 - 4)*t, 4*t**2 + 2*x**2 + 4)

