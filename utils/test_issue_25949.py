
def test_issue_25949():
    from sympy.core.symbol import symbols
    y = symbols("y", nonzero=True)
    assert integrate(cosh(y*(x + 1)), (x, -1, -0.25), meijerg=True) == sinh(0.75*y)/y

