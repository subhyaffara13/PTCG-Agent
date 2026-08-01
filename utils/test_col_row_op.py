
def test_col_row_op():
    M = Matrix([[x, 0, 0],
                [0, y, 0]])
    M.row_op(1, lambda r, j: r + j + 1)
    assert M == Matrix([[x,     0, 0],
                        [1, y + 2, 3]])

    M.col_op(0, lambda c, j: c + y**j)
    assert M == Matrix([[x + 1,     0, 0],
                        [1 + y, y + 2, 3]])

    # neither row nor slice give copies that allow the original matrix to
    # be changed
    assert M.row(0) == Matrix([[x + 1, 0, 0]])
    r1 = M.row(0)
    r1[0] = 42
    assert M[0, 0] == x + 1
    r1 = M[0, :-1]  # also testing negative slice
    r1[0] = 42
    assert M[0, 0] == x + 1
    c1 = M.col(0)
    assert c1 == Matrix([x + 1, 1 + y])
    c1[0] = 0
    assert M[0, 0] == x + 1
    c1 = M[:, 0]
    c1[0] = 42
    assert M[0, 0] == x + 1


def test_col_row_op():
    M = Matrix([[x, 0, 0],
                [0, y, 0]])
    M.row_op(1, lambda r, j: r + j + 1)
    assert M == Matrix([[x,     0, 0],
                        [1, y + 2, 3]])

    M.col_op(0, lambda c, j: c + y**j)
    assert M == Matrix([[x + 1,     0, 0],
                        [1 + y, y + 2, 3]])

    # neither row nor slice give copies that allow the original matrix to
    # be changed
    assert M.row(0) == Matrix([[x + 1, 0, 0]])
    r1 = M.row(0)
    r1[0] = 42
    assert M[0, 0] == x + 1
    r1 = M[0, :-1]  # also testing negative slice
    r1[0] = 42
    assert M[0, 0] == x + 1
    c1 = M.col(0)
    assert c1 == Matrix([x + 1, 1 + y])
    c1[0] = 0
    assert M[0, 0] == x + 1
    c1 = M[:, 0]
    c1[0] = 42
    assert M[0, 0] == x + 1

