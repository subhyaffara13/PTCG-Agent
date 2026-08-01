
def test_issue_22189():
    x = Symbol('x')
    for a in (sqrt(7 - 2*x) - 2, 1 - x):
        assert Abs(a) - Abs(-a) == 0, a

