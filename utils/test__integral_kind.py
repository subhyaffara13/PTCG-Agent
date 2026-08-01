
def test_Integral_kind():
    A = MatrixSymbol('A', 2,2)
    assert Integral(comm_x, comm_x).kind is NumberKind
    assert Integral(A, comm_x).kind is MatrixKind(NumberKind)

