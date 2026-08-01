
def test_non_matmul():
    """
    Test that if explicitly specified as non-matrix, mul reverts
    to scalar multiplication.
    """
    class foo(Expr):
        is_Matrix=False
        is_MatrixLike=False
        shape = (1, 1)

    A = Matrix([[1, 2], [3, 4]])
    b = foo()
    assert b*A == Matrix([[b, 2*b], [3*b, 4*b]])
    assert A*b == Matrix([[b, 2*b], [3*b, 4*b]])


def test_non_matmul():
    """
    Test that if explicitly specified as non-matrix, mul reverts
    to scalar multiplication.
    """
    class foo(Expr):
        is_Matrix=False
        is_MatrixLike=False
        shape = (1, 1)

    A = Matrix([[1, 2], [3, 4]])
    b = foo()
    assert b*A == Matrix([[b, 2*b], [3*b, 4*b]])
    assert A*b == Matrix([[b, 2*b], [3*b, 4*b]])

