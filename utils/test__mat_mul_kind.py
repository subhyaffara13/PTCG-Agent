
def test_MatMul_kind():
    M = Matrix([[1,2],[3,4]])
    assert MatMul(2, M).kind is MatrixKind(NumberKind)
    assert MatMul(comm_x, M).kind is MatrixKind(NumberKind)

