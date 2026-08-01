
def test_issue_12638():
    from sympy.abc import a, b, c
    assert Min(a, b, c, Max(a, b)) == Min(a, b, c)
    assert Min(a, b, Max(a, b, c)) == Min(a, b)
    assert Min(a, b, Max(a, c)) == Min(a, b)

