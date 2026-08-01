
def test_pretty_Determinant():
    from sympy.matrices import Determinant, Inverse, BlockMatrix, OneMatrix, ZeroMatrix
    m = Matrix(((1, 2), (3, 4)))
    assert upretty(Determinant(m)) == '│1  2│\n│    │\n│3  4│'
    assert upretty(Determinant(Inverse(m))) == \
        '│      -1│\n'\
        '│⎡1  2⎤  │\n'\
        '│⎢    ⎥  │\n'\
        '│⎣3  4⎦  │'
    X = MatrixSymbol('X', 2, 2)
    assert upretty(Determinant(X)) == '│X│'
    assert upretty(Determinant(X + m)) == \
        '│⎡1  2⎤    │\n'\
        '│⎢    ⎥ + X│\n'\
        '│⎣3  4⎦    │'
    assert upretty(Determinant(BlockMatrix(((OneMatrix(2, 2), X),
                                            (m, ZeroMatrix(2, 2)))))) == \
        '│  𝟙     X│\n'\
        '│         │\n'\
        '│⎡1  2⎤   │\n'\
        '│⎢    ⎥  𝟘│\n'\
        '│⎣3  4⎦   │'

