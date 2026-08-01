
def test_issue_12780():
    n = symbols("n")
    i = Idx("i", (0, n))
    raises(TypeError, lambda: i.subs(n, 1.5))

