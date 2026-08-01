
def test_issue_4203():
    assert cse(sin(x**x)/x**x) == ([(x0, x**x)], [sin(x0)/x0])

