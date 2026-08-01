
def test_minmax_no_evaluate():
    from sympy import evaluate
    p = Symbol('p', positive=True)

    assert Max(1, 3) == 3
    assert Max(1, 3).args == ()
    assert Max(0, p) == p
    assert Max(0, p).args == ()
    assert Min(0, p) == 0
    assert Min(0, p).args == ()

    assert Max(1, 3, evaluate=False) != 3
    assert Max(1, 3, evaluate=False).args == (1, 3)
    assert Max(0, p, evaluate=False) != p
    assert Max(0, p, evaluate=False).args == (0, p)
    assert Min(0, p, evaluate=False) != 0
    assert Min(0, p, evaluate=False).args == (0, p)

    with evaluate(False):
        assert Max(1, 3) != 3
        assert Max(1, 3).args == (1, 3)
        assert Max(0, p) != p
        assert Max(0, p).args == (0, p)
        assert Min(0, p) != 0
        assert Min(0, p).args == (0, p)

