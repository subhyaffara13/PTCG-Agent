
def test_Derivative_kind():
    A = MatrixSymbol('A', 2,2)
    assert Derivative(comm_x, comm_x).kind is NumberKind
    assert Derivative(A, comm_x).kind is MatrixKind(NumberKind)

