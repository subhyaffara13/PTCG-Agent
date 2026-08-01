
def test_multivariate_variance():
    raises(ShapeError, lambda: Variance(A))

    expr = Variance(a)
    assert expr == Variance(a) == VarianceMatrix(a)
    assert expr.expand() == ZeroMatrix(k, k)
    expr = Variance(a.T)
    assert expr == Variance(a.T) == VarianceMatrix(a.T)
    assert expr.expand() == ZeroMatrix(k, k)

    expr = Variance(X)
    assert expr == Variance(X) == VarianceMatrix(X)
    assert expr.shape == (k, k)
    assert expr.rows == k
    assert expr.cols == k
    assert isinstance(expr, VarianceMatrix)

    expr = Variance(A*X)
    assert expr == VarianceMatrix(A*X)
    assert expr.expand() == A*VarianceMatrix(X)*A.T
    assert isinstance(expr, VarianceMatrix)
    assert expr.shape == (k, k)

    expr = Variance(A*B*X)
    assert expr.expand() == A*B*VarianceMatrix(X)*B.T*A.T

    expr = Variance(m1*X2)
    assert expr.expand() == expr

    expr = Variance(A2*m1*B2*X2)
    assert expr.args[0].args == (A2, m1, B2, X2)
    assert expr.expand() == expr

    expr = Variance(A*X + B*Y)
    assert expr.expand() == 2*A*CrossCovarianceMatrix(X, Y)*B.T +\
                    A*VarianceMatrix(X)*A.T + B*VarianceMatrix(Y)*B.T

