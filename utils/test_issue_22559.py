
def test_issue_22559():
    alpha = AlgebraicNumber(sqrt(2))
    assert minimal_polynomial(alpha**3, x) == x**2 - 8

