
def test_echelon_form():
    # echelon form is not unique, but the result
    # must be row-equivalent to the original matrix
    # and it must be in echelon form.

    a = zeros_Reductions(3)
    e = eye_Reductions(3)

    # we can assume the zero matrix and the identity matrix shouldn't change
    assert a.echelon_form() == a
    assert e.echelon_form() == e

    a = ReductionsOnlyMatrix(0, 0, [])
    assert a.echelon_form() == a

    a = ReductionsOnlyMatrix(1, 1, [5])
    assert a.echelon_form() == a

    # now we get to the real tests

    def verify_row_null_space(mat, rows, nulls):
        for v in nulls:
            assert all(t.is_zero for t in a_echelon*v)
        for v in rows:
            if not all(t.is_zero for t in v):
                assert not all(t.is_zero for t in a_echelon*v.transpose())

    a = ReductionsOnlyMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    nulls = [Matrix([
                     [ 1],
                     [-2],
                     [ 1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)


    a = ReductionsOnlyMatrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 8])
    nulls = []
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = ReductionsOnlyMatrix(3, 3, [2, 1, 3, 0, 0, 0, 2, 1, 3])
    nulls = [Matrix([
             [Rational(-1, 2)],
             [   1],
             [   0]]),
             Matrix([
             [Rational(-3, 2)],
             [   0],
             [   1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    # this one requires a row swap
    a = ReductionsOnlyMatrix(3, 3, [2, 1, 3, 0, 0, 0, 1, 1, 3])
    nulls = [Matrix([
             [   0],
             [  -3],
             [   1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = ReductionsOnlyMatrix(3, 3, [0, 3, 3, 0, 2, 2, 0, 1, 1])
    nulls = [Matrix([
             [1],
             [0],
             [0]]),
             Matrix([
             [ 0],
             [-1],
             [ 1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = ReductionsOnlyMatrix(2, 3, [2, 2, 3, 3, 3, 0])
    nulls = [Matrix([
             [-1],
             [1],
             [0]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)


def test_echelon_form():
    # echelon form is not unique, but the result
    # must be row-equivalent to the original matrix
    # and it must be in echelon form.

    a = zeros(3)
    e = eye(3)

    # we can assume the zero matrix and the identity matrix shouldn't change
    assert a.echelon_form() == a
    assert e.echelon_form() == e

    a = Matrix(0, 0, [])
    assert a.echelon_form() == a

    a = Matrix(1, 1, [5])
    assert a.echelon_form() == a

    # now we get to the real tests

    def verify_row_null_space(mat, rows, nulls):
        for v in nulls:
            assert all(t.is_zero for t in a_echelon*v)
        for v in rows:
            if not all(t.is_zero for t in v):
                assert not all(t.is_zero for t in a_echelon*v.transpose())

    a = Matrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    nulls = [Matrix([
                     [ 1],
                     [-2],
                     [ 1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)


    a = Matrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 8])
    nulls = []
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = Matrix(3, 3, [2, 1, 3, 0, 0, 0, 2, 1, 3])
    nulls = [Matrix([
             [Rational(-1, 2)],
             [   1],
             [   0]]),
             Matrix([
             [Rational(-3, 2)],
             [   0],
             [   1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    # this one requires a row swap
    a = Matrix(3, 3, [2, 1, 3, 0, 0, 0, 1, 1, 3])
    nulls = [Matrix([
             [   0],
             [  -3],
             [   1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = Matrix(3, 3, [0, 3, 3, 0, 2, 2, 0, 1, 1])
    nulls = [Matrix([
             [1],
             [0],
             [0]]),
             Matrix([
             [ 0],
             [-1],
             [ 1]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

    a = Matrix(2, 3, [2, 2, 3, 3, 3, 0])
    nulls = [Matrix([
             [-1],
             [1],
             [0]])]
    rows = [a[i, :] for i in range(a.rows)]
    a_echelon = a.echelon_form()
    assert a_echelon.is_echelon
    verify_row_null_space(a, rows, nulls)

