
def test_matrix_expression_to_indices():
    i, j = symbols("i, j")
    i1, i2, i3 = symbols("i_1:4")

    def replace_dummies(expr):
        repl = {i: Symbol(i.name) for i in expr.atoms(Dummy)}
        return expr.xreplace(repl)

    expr = W*X*Z
    assert replace_dummies(expr._entry(i, j)) == \
        Sum(W[i, i1]*X[i1, i2]*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1))
    assert MatrixExpr.from_index_summation(expr._entry(i, j)) == expr

    expr = Z.T*X.T*W.T
    assert replace_dummies(expr._entry(i, j)) == \
        Sum(W[j, i2]*X[i2, i1]*Z[i1, i], (i1, 0, m-1), (i2, 0, l-1))
    assert MatrixExpr.from_index_summation(expr._entry(i, j), i) == expr

    expr = W*X*Z + W*Y*Z
    assert replace_dummies(expr._entry(i, j)) == \
        Sum(W[i, i1]*X[i1, i2]*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1)) +\
        Sum(W[i, i1]*Y[i1, i2]*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1))
    assert MatrixExpr.from_index_summation(expr._entry(i, j)) == expr

    expr = 2*W*X*Z + 3*W*Y*Z
    assert replace_dummies(expr._entry(i, j)) == \
        2*Sum(W[i, i1]*X[i1, i2]*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1)) +\
        3*Sum(W[i, i1]*Y[i1, i2]*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1))
    assert MatrixExpr.from_index_summation(expr._entry(i, j)) == expr

    expr = W*(X + Y)*Z
    assert replace_dummies(expr._entry(i, j)) == \
            Sum(W[i, i1]*(X[i1, i2] + Y[i1, i2])*Z[i2, j], (i1, 0, l-1), (i2, 0, m-1))
    assert MatrixExpr.from_index_summation(expr._entry(i, j)) == expr

    expr = A*B**2*A
    #assert replace_dummies(expr._entry(i, j)) == \
    #        Sum(A[i, i1]*B[i1, i2]*B[i2, i3]*A[i3, j], (i1, 0, 1), (i2, 0, 1), (i3, 0, 1))

    # Check that different dummies are used in sub-multiplications:
    expr = (X1*X2 + X2*X1)*X3
    assert replace_dummies(expr._entry(i, j)) == \
           Sum((Sum(X1[i, i2] * X2[i2, i1], (i2, 0, m - 1)) + Sum(X1[i3, i1] * X2[i, i3], (i3, 0, m - 1))) * X3[
               i1, j], (i1, 0, m - 1))

