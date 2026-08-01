
def test_deprecated_mat_smat():
    for cls in Matrix, ImmutableMatrix:
        m = cls.zeros(3, 2)
        with warns_deprecated_sympy():
            mat = m._mat
        assert mat == m.flat()
    for cls in SparseMatrix, ImmutableSparseMatrix:
        m = cls.zeros(3, 2)
        with warns_deprecated_sympy():
            smat = m._smat
        assert smat == m.todok()


def test_deprecated_mat_smat():
    for cls in Matrix, ImmutableMatrix:
        m = cls.zeros(3, 2)
        with warns_deprecated_sympy():
            mat = m._mat
        assert mat == m.flat()
    for cls in SparseMatrix, ImmutableSparseMatrix:
        m = cls.zeros(3, 2)
        with warns_deprecated_sympy():
            smat = m._smat
        assert smat == m.todok()

