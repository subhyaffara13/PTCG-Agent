
def test_matexpr_subs():
    A = MatrixSymbol('A', n, m)
    B = MatrixSymbol('B', m, l)
    C = MatrixSymbol('C', m, l)

    assert A.subs(n, m).shape == (m, m)
    assert (A*B).subs(B, C) == A*C
    assert (A*B).subs(l, n).is_square

    W = MatrixSymbol("W", 3, 3)
    X = MatrixSymbol("X", 2, 2)
    Y = MatrixSymbol("Y", 1, 2)
    Z = MatrixSymbol("Z", n, 2)
    # no restrictions on Symbol replacement
    assert X.subs(X, Y) == Y
    # it might be better to just change the name
    y = Str('y')
    assert X.subs(Str("X"), y).args == (y, 2, 2)
    # it's ok to introduce a wider matrix
    assert X[1, 1].subs(X, W) == W[1, 1]
    # but for a given MatrixExpression, only change
    # name if indexing on the new shape is valid.
    # Here, X is 2,2; Y is 1,2 and Y[1, 1] is out
    # of range so an error is raised
    raises(IndexError, lambda: X[1, 1].subs(X, Y))
    # here, [0, 1] is in range so the subs succeeds
    assert X[0, 1].subs(X, Y) == Y[0, 1]
    # and here the size of n will accept any index
    # in the first position
    assert W[2, 1].subs(W, Z) == Z[2, 1]
    # but not in the second position
    raises(IndexError, lambda: W[2, 2].subs(W, Z))
    # any matrix should raise if invalid
    raises(IndexError, lambda: W[2, 2].subs(W, zeros(2)))

    A = SparseMatrix([[1, 2], [3, 4]])
    B = Matrix([[1, 2], [3, 4]])
    C, D = MatrixSymbol('C', 2, 2), MatrixSymbol('D', 2, 2)

    assert (C*D).subs({C: A, D: B}) == MatMul(A, B)

