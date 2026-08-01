
def test_Determinant():
    from sympy.matrices import Determinant, Inverse, BlockMatrix, OneMatrix, ZeroMatrix
    m = Matrix(((1, 2), (3, 4)))
    assert latex(Determinant(m)) == '\\left|{\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}}\\right|'
    assert latex(Determinant(Inverse(m))) == \
        '\\left|{\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right]^{-1}}\\right|'
    X = MatrixSymbol('X', 2, 2)
    assert latex(Determinant(X)) == '\\left|{X}\\right|'
    assert latex(Determinant(X + m)) == \
        '\\left|{\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] + X}\\right|'
    assert latex(Determinant(BlockMatrix(((OneMatrix(2, 2), X),
                                          (m, ZeroMatrix(2, 2)))))) == \
        '\\left|{\\begin{matrix}1 & X\\\\\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] & 0\\end{matrix}}\\right|'

