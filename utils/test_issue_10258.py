
def test_issue_10258():
    assert Piecewise((0, x < 1), (1, True)).is_zero is None
    assert Piecewise((-1, x < 1), (1, True)).is_zero is False
    a = Symbol('a', zero=True)
    assert Piecewise((0, x < 1), (a, True)).is_zero
    assert Piecewise((1, x < 1), (a, x < 3)).is_zero is None
    a = Symbol('a')
    assert Piecewise((0, x < 1), (a, True)).is_zero is None
    assert Piecewise((0, x < 1), (1, True)).is_nonzero is None
    assert Piecewise((1, x < 1), (2, True)).is_nonzero
    assert Piecewise((0, x < 1), (oo, True)).is_finite is None
    assert Piecewise((0, x < 1), (1, True)).is_finite
    b = Basic()
    assert Piecewise((b, x < 1)).is_finite is None

    # 10258
    c = Piecewise((1, x < 0), (2, True)) < 3
    assert c != True
    assert piecewise_fold(c) == True

