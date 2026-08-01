
def test_curry_simple():
    cmul = curry(mul)
    double = cmul(2)
    assert callable(double)
    assert double(10) == 20
    assert repr(cmul) == repr(mul)

    cmap = curry(map)
    assert list(cmap(inc)([1, 2, 3])) == [2, 3, 4]

    assert raises(TypeError, lambda: curry())
    assert raises(TypeError, lambda: curry({1: 2}))

