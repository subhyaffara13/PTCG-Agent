
def test_issue_8413():
    x = Symbol('x', real=True)
    # we can't evaluate in general because non-reals are not
    # comparable: Min(floor(3.2 + I), 3.2 + I) -> ValueError
    assert Min(floor(x), x) == floor(x)
    assert Min(ceiling(x), x) == x
    assert Max(floor(x), x) == x
    assert Max(ceiling(x), x) == ceiling(x)

