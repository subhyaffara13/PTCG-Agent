
def test_PolyElement___call__():
    R, x = ring("x", ZZ)
    f = 3*x + 1

    assert f(0) == 1
    assert f(1) == 4

    raises(ValueError, lambda: f())
    raises(ValueError, lambda: f(0, 1))

    raises(CoercionFailed, lambda: f(QQ(1,7)))

    R, x,y = ring("x,y", ZZ)
    f = 3*x + y**2 + 1

    assert f(0, 0) == 1
    assert f(1, 7) == 53

    Ry = R.drop(x)

    assert f(0) == Ry.y**2 + 1
    assert f(1) == Ry.y**2 + 4

    raises(ValueError, lambda: f())
    raises(ValueError, lambda: f(0, 1, 2))

    raises(CoercionFailed, lambda: f(1, QQ(1,7)))
    raises(CoercionFailed, lambda: f(QQ(1,7), 1))
    raises(CoercionFailed, lambda: f(QQ(1,7), QQ(1,7)))

