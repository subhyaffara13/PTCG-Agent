
def test_issue_13396():
    expr = -2*y*exp(-x**2 - y**2)*Abs(x)
    sol = FiniteSet(0)

    assert solveset(expr, y, domain=S.Reals) == sol

    # Related type of equation also solved here
    assert solveset(atan(x**2 - y**2)-pi/2, y, S.Reals) is S.EmptySet

