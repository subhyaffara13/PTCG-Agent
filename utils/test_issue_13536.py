
def test_issue_13536():
    from sympy.core.symbol import Symbol
    a = Symbol('a', positive=True)
    assert integrate(1/x**2, (x, oo, a)) == -1/a

