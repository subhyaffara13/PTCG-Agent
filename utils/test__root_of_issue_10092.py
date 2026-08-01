
def test_RootOf_issue_10092():
    x = Symbol('x', real=True)
    eq = x**3 - 17*x**2 + 81*x - 118
    r = RootOf(eq, 0)
    assert (x < r).subs(x, r) is S.false

