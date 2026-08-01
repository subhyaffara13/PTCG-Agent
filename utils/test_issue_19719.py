
def test_issue_19719():
    a, b = symbols('a, b')
    expr = a**2 * (b + 1) + (7 + 1/b)/a
    collected = collect(expr, (a**2, 1/a), evaluate=False)
    # Would return {_Dummy_20**(-2): b + 1, 1/a: 7 + 1/b} without xreplace
    assert collected == {a**2: b + 1, 1/a: 7 + 1/b}

