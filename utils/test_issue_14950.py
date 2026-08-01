
def test_issue_14950():
    x = Matrix(symbols('t s'))
    x0 = Matrix([17, 23])
    eqn = x + x0
    assert nsolve(eqn, x, x0) == nfloat(-x0)
    assert nsolve(eqn.T, x.T, x0.T) == nfloat(-x0)

