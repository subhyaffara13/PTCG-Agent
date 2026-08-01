
def test_zero_not_false():
    # https://github.com/sympy/sympy/issues/20796
    assert (S(0.0) == S.false) is False
    assert (S.false == S(0.0)) is False
    assert (S(0) == S.false) is False
    assert (S.false == S(0)) is False

