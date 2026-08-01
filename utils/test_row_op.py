
def test_row_op():
    e = eye_Reductions(3)

    raises(ValueError, lambda: e.elementary_row_op("abc"))
    raises(ValueError, lambda: e.elementary_row_op())
    raises(ValueError, lambda: e.elementary_row_op('n->kn', row=5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->kn', row=-5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=1, row2=5))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=5, row2=1))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=-5, row2=1))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=1, row2=-5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=5, row2=1, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=-5, row2=1, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=-5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=1, k=5))

    # test various ways to set arguments
    assert e.elementary_row_op("n->kn", 0, 5) == Matrix([[5, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", 1, 5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", row=1, k=5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", row1=1, k=5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", 0, 1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", row1=0, row2=1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", row=0, row2=1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", 0, 5, 1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", row=0, k=5, row2=1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", row1=0, k=5, row2=1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])

    # make sure the matrix doesn't change size
    a = ReductionsOnlyMatrix(2, 3, [0]*6)
    assert a.elementary_row_op("n->kn", 1, 5) == Matrix(2, 3, [0]*6)
    assert a.elementary_row_op("n<->m", 0, 1) == Matrix(2, 3, [0]*6)
    assert a.elementary_row_op("n->n+km", 0, 5, 1) == Matrix(2, 3, [0]*6)


def test_row_op():
    e = eye(3)

    raises(ValueError, lambda: e.elementary_row_op("abc"))
    raises(ValueError, lambda: e.elementary_row_op())
    raises(ValueError, lambda: e.elementary_row_op('n->kn', row=5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->kn', row=-5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=1, row2=5))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=5, row2=1))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=-5, row2=1))
    raises(ValueError, lambda: e.elementary_row_op('n<->m', row1=1, row2=-5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=5, row2=1, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=-5, row2=1, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=-5, k=5))
    raises(ValueError, lambda: e.elementary_row_op('n->n+km', row1=1, row2=1, k=5))

    # test various ways to set arguments
    assert e.elementary_row_op("n->kn", 0, 5) == Matrix([[5, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", 1, 5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", row=1, k=5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->kn", row1=1, k=5) == Matrix([[1, 0, 0], [0, 5, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", 0, 1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", row1=0, row2=1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n<->m", row=0, row2=1) == Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", 0, 5, 1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", row=0, k=5, row2=1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])
    assert e.elementary_row_op("n->n+km", row1=0, k=5, row2=1) == Matrix([[1, 5, 0], [0, 1, 0], [0, 0, 1]])

    # make sure the matrix doesn't change size
    a = Matrix(2, 3, [0]*6)
    assert a.elementary_row_op("n->kn", 1, 5) == Matrix(2, 3, [0]*6)
    assert a.elementary_row_op("n<->m", 0, 1) == Matrix(2, 3, [0]*6)
    assert a.elementary_row_op("n->n+km", 0, 5, 1) == Matrix(2, 3, [0]*6)

