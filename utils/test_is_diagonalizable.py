
def test_is_diagonalizable():
    a, b, c = symbols('a b c')
    m = Matrix(2, 2, [a, c, c, b])
    assert m.is_symmetric()
    assert m.is_diagonalizable()
    assert not Matrix(2, 2, [1, 1, 0, 1]).is_diagonalizable()

    m = Matrix(2, 2, [0, -1, 1, 0])
    assert m.is_diagonalizable()
    assert not m.is_diagonalizable(reals_only=True)

