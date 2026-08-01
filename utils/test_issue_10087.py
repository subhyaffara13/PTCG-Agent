
def test_issue_10087():
    a, b = Piecewise((x, x > 1), (2, True)), Piecewise((x, x > 3), (3, True))
    m = a*b
    f = piecewise_fold(m)
    for i in (0, 2, 4):
        assert m.subs(x, i) == f.subs(x, i)
    m = a + b
    f = piecewise_fold(m)
    for i in (0, 2, 4):
        assert m.subs(x, i) == f.subs(x, i)

