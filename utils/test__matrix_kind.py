
def test_Matrix_kind():
    classes = (Matrix, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix)
    for cls in classes:
        m = cls.zeros(3, 2)
        assert m.kind is MatrixKind(NumberKind)

