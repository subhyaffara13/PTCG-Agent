
def test_SetKind_MatrixSet():
    assert MatrixSet(2, 2, set=S.Reals).kind is SetKind(MatrixKind(NumberKind))

