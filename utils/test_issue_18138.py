
def test_issue_18138():
    eq = x**2 - x - y**2
    v = (x, y)
    for sol in diophantine(eq):
        assert not diop_simplify(eq.xreplace(dict(zip(v, sol))))

