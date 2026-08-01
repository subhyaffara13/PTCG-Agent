
def test_det_quick():
    m = Matrix(3, 3, symbols('a:9'))
    assert m.det() == det_quick(m)  # calls det_perm
    m[0, 0] = 1
    assert m.det() == det_quick(m)  # calls det_minor
    m = Matrix(3, 3, list(range(9)))
    assert m.det() == det_quick(m)  # defaults to .det()
    # make sure they work with Sparse
    s = SparseMatrix(2, 2, (1, 2, 1, 4))
    assert det_perm(s) == det_minor(s) == s.det()

