
def test_issue_10337():
    assert (FiniteSet(2) == 3) is False
    assert (FiniteSet(2) != 3) is True
    raises(TypeError, lambda: FiniteSet(2) < 3)
    raises(TypeError, lambda: FiniteSet(2) <= 3)
    raises(TypeError, lambda: FiniteSet(2) > 3)
    raises(TypeError, lambda: FiniteSet(2) >= 3)

