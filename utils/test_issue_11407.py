
def test_issue_11407():
    a, b, c, x = symbols('a b c x')
    assert series(sqrt(a + b + c*x), x, 0, 1) == sqrt(a + b) + O(x)
    assert series(sqrt(a + b + c + c*x), x, 0, 1) == sqrt(a + b + c) + O(x)

