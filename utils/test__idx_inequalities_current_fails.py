
def test_Idx_inequalities_current_fails():
    i14 = Idx("i14", (1, 4))

    assert S(5) >= i14
    assert S(5) > i14
    assert not (S(5) <= i14)
    assert not (S(5) < i14)

