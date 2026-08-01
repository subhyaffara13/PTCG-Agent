
def test_issue_12283():
    x = symbols('x')
    X = RandomSymbol(x)
    Y = RandomSymbol('Y')
    Z = RandomMatrixSymbol('Z', 2, 1)
    W = RandomMatrixSymbol('W', 2, 1)
    RI = RandomIndexedSymbol(Indexed('RI', 3))
    assert pspace(Z) == PSpace()
    assert pspace(RI) == PSpace()
    assert pspace(X) == PSpace()
    assert E(X) == Expectation(X)
    assert P(Y > 3) == Probability(Y > 3)
    assert variance(X) == Variance(X)
    assert variance(RI) == Variance(RI)
    assert covariance(X, Y) == Covariance(X, Y)
    assert covariance(W, Z) == Covariance(W, Z)

