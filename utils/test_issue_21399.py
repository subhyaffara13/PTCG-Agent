
def test_issue_21399():
    from sympy.abc import a, b, c
    assert Max(Min(a, b), Min(a, b, c)) == Min(a, b)

