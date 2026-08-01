
def test_sympy__codegen__matrix_nodes__MatrixSolve():
    from sympy.matrices import MatrixSymbol
    from sympy.codegen.matrix_nodes import MatrixSolve
    A = MatrixSymbol('A', 3, 3)
    v = MatrixSymbol('x', 3, 1)
    assert _test_args(MatrixSolve(A, v))

