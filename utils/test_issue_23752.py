
def test_issue_23752():
    expr1 = sqrt(-I*x**2 + x - 3)
    expr2 = sqrt(-I*x**2 + I*x - 3)
    assert limit(expr1, x, 0, '+') == -sqrt(3)*I
    assert limit(expr1, x, 0, '-') == -sqrt(3)*I
    assert limit(expr2, x, 0, '+') == sqrt(3)*I
    assert limit(expr2, x, 0, '-') == -sqrt(3)*I

