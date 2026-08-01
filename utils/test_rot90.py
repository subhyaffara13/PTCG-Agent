
def test_rot90():
    A = Matrix([[1, 2], [3, 4]])
    assert A == A.rot90(0) == A.rot90(4)
    assert A.rot90(2) == A.rot90(-2) == A.rot90(6) == Matrix(((4, 3), (2, 1)))
    assert A.rot90(3) == A.rot90(-1) == A.rot90(7) == Matrix(((2, 4), (1, 3)))
    assert A.rot90() == A.rot90(-7) == A.rot90(-3) == Matrix(((3, 1), (4, 2)))


def test_rot90():
    A = Matrix([[1, 2], [3, 4]])
    assert A == A.rot90(0) == A.rot90(4)
    assert A.rot90(2) == A.rot90(-2) == A.rot90(6) == Matrix(((4, 3), (2, 1)))
    assert A.rot90(3) == A.rot90(-1) == A.rot90(7) == Matrix(((2, 4), (1, 3)))
    assert A.rot90() == A.rot90(-7) == A.rot90(-3) == Matrix(((3, 1), (4, 2)))

