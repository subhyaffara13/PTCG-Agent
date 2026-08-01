
def test_issue_9106():
    eq = -48 - 2*x*(3*x - 1) + y*(3*y - 1)
    v = (x, y)
    for sol in diophantine(eq):
        assert not diop_simplify(eq.xreplace(dict(zip(v, sol))))

