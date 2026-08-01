
def test_issue_22849():
    a = -8 + 3 * sqrt(3)
    x = AlgebraicNumber(a)
    assert evalf(a, 1, {}) == evalf(x, 1, {})

