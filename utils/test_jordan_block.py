
def test_jordan_block():
    assert SpecialOnlyMatrix.jordan_block(3, 2) == SpecialOnlyMatrix.jordan_block(3, eigenvalue=2) \
            == SpecialOnlyMatrix.jordan_block(size=3, eigenvalue=2) \
            == SpecialOnlyMatrix.jordan_block(3, 2, band='upper') \
            == SpecialOnlyMatrix.jordan_block(
                size=3, eigenval=2, eigenvalue=2) \
            == Matrix([
                [2, 1, 0],
                [0, 2, 1],
                [0, 0, 2]])

    assert SpecialOnlyMatrix.jordan_block(3, 2, band='lower') == Matrix([
                    [2, 0, 0],
                    [1, 2, 0],
                    [0, 1, 2]])
    # missing eigenvalue
    raises(ValueError, lambda: SpecialOnlyMatrix.jordan_block(2))
    # non-integral size
    raises(ValueError, lambda: SpecialOnlyMatrix.jordan_block(3.5, 2))
    # size not specified
    raises(ValueError, lambda: SpecialOnlyMatrix.jordan_block(eigenvalue=2))
    # inconsistent eigenvalue
    raises(ValueError,
    lambda: SpecialOnlyMatrix.jordan_block(
        eigenvalue=2, eigenval=4))

    # Using alias keyword
    assert SpecialOnlyMatrix.jordan_block(size=3, eigenvalue=2) == \
        SpecialOnlyMatrix.jordan_block(size=3, eigenval=2)


def test_jordan_block():
    assert Matrix.jordan_block(3, 2) == Matrix.jordan_block(3, eigenvalue=2) \
            == Matrix.jordan_block(size=3, eigenvalue=2) \
            == Matrix.jordan_block(3, 2, band='upper') \
            == Matrix.jordan_block(
                size=3, eigenval=2, eigenvalue=2) \
            == Matrix([
                [2, 1, 0],
                [0, 2, 1],
                [0, 0, 2]])

    assert Matrix.jordan_block(3, 2, band='lower') == Matrix([
                    [2, 0, 0],
                    [1, 2, 0],
                    [0, 1, 2]])
    # missing eigenvalue
    raises(ValueError, lambda: Matrix.jordan_block(2))
    # non-integral size
    raises(ValueError, lambda: Matrix.jordan_block(3.5, 2))
    # size not specified
    raises(ValueError, lambda: Matrix.jordan_block(eigenvalue=2))
    # inconsistent eigenvalue
    raises(ValueError,
    lambda: Matrix.jordan_block(
        eigenvalue=2, eigenval=4))

    # Using alias keyword
    assert Matrix.jordan_block(size=3, eigenvalue=2) == \
        Matrix.jordan_block(size=3, eigenval=2)

