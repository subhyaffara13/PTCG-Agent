
def test_array_expr_reshape():

    A = MatrixSymbol("A", 2, 2)
    B = ArraySymbol("B", (2, 2, 2))
    C = Array([1, 2, 3, 4])

    expr = Reshape(A, (4,))
    assert expr.expr == A
    assert expr.shape == (4,)
    assert expr.as_explicit() == Array([A[0, 0], A[0, 1], A[1, 0], A[1, 1]])

    expr = Reshape(B, (2, 4))
    assert expr.expr == B
    assert expr.shape == (2, 4)
    ee = expr.as_explicit()
    assert isinstance(ee, ImmutableDenseNDimArray)
    assert ee.shape == (2, 4)
    assert ee == Array([[B[0, 0, 0], B[0, 0, 1], B[0, 1, 0], B[0, 1, 1]], [B[1, 0, 0], B[1, 0, 1], B[1, 1, 0], B[1, 1, 1]]])

    expr = Reshape(A, (k, 2))
    assert expr.shape == (k, 2)

    raises(ValueError, lambda: Reshape(A, (2, 3)))
    raises(ValueError, lambda: Reshape(A, (3,)))

    expr = Reshape(C, (2, 2))
    assert expr.expr == C
    assert expr.shape == (2, 2)
    assert expr.doit() == Array([[1, 2], [3, 4]])

