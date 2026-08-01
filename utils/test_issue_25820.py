
def test_issue_25820():
    x = Symbol('x')
    y = Function('y')
    eq = y(x)**3*y(x).diff(x, 2) + 49
    assert dsolve(eq, y(x)) is not None  # doesn't raise

