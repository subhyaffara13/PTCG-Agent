
def test_invertible_check():
    # sometimes a singular matrix will have a pivot vector shorter than
    # the number of rows in a matrix...
    assert Matrix([[1, 2], [1, 2]]).rref() == (Matrix([[1, 2], [0, 0]]), (0,))
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inv())
    m = Matrix([
        [-1, -1,  0],
        [ x,  1,  1],
        [ 1,  x, -1],
    ])
    assert len(m.rref()[1]) != m.rows
    # in addition, unless simplify=True in the call to rref, the identity
    # matrix will be returned even though m is not invertible
    assert m.rref()[0] != eye(3)
    assert m.rref(simplify=signsimp)[0] != eye(3)
    raises(ValueError, lambda: m.inv(method="ADJ"))
    raises(ValueError, lambda: m.inv(method="GE"))
    raises(ValueError, lambda: m.inv(method="LU"))


def test_invertible_check():
    # sometimes a singular matrix will have a pivot vector shorter than
    # the number of rows in a matrix...
    assert Matrix([[1, 2], [1, 2]]).rref() == (Matrix([[1, 2], [0, 0]]), (0,))
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inv())
    m = Matrix([
        [-1, -1,  0],
        [ x,  1,  1],
        [ 1,  x, -1],
    ])
    assert len(m.rref()[1]) != m.rows
    # in addition, unless simplify=True in the call to rref, the identity
    # matrix will be returned even though m is not invertible
    assert m.rref()[0] != eye(3)
    assert m.rref(simplify=signsimp)[0] != eye(3)
    raises(ValueError, lambda: m.inv(method="ADJ"))
    raises(ValueError, lambda: m.inv(method="GE"))
    raises(ValueError, lambda: m.inv(method="LU"))

