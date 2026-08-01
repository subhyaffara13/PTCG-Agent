
def test_Transpose():
    assert isinstance(aesara_code_(X.T).owner.op, DimShuffle)


def test_Transpose():
    from sympy.matrices import Transpose, MatPow, HadamardPower
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert latex(Transpose(X)) == r'X^{T}'
    assert latex(Transpose(X + Y)) == r'\left(X + Y\right)^{T}'

    assert latex(Transpose(HadamardPower(X, 2))) == r'\left(X^{\circ {2}}\right)^{T}'
    assert latex(HadamardPower(Transpose(X), 2)) == r'\left(X^{T}\right)^{\circ {2}}'
    assert latex(Transpose(MatPow(X, 2))) == r'\left(X^{2}\right)^{T}'
    assert latex(MatPow(Transpose(X), 2)) == r'\left(X^{T}\right)^{2}'
    m = Matrix(((1, 2), (3, 4)))
    assert latex(Transpose(m)) == '\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right]^{T}'
    assert latex(Transpose(m+X)) == \
        '\\left(\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] + X\\right)^{T}'
    from sympy.matrices import BlockMatrix, OneMatrix, ZeroMatrix
    assert latex(Transpose(BlockMatrix(((OneMatrix(2, 2), X),
                                        (m, ZeroMatrix(2, 2)))))) == \
        '\\left[\\begin{matrix}1 & X\\\\\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] & 0\\end{matrix}\\right]^{T}'
    # Issue 20959
    Mx = MatrixSymbol('M^x', 2, 2)
    assert latex(Transpose(Mx)) == r'\left(M^{x}\right)^{T}'


def test_Transpose():
    assert isinstance(theano_code_(X.T).owner.op, tt.DimShuffle)


def test_Transpose():
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert pretty(Transpose(X)) == " T\nX "
    assert pretty(Transpose(X + Y)) == "       T\n(X + Y) "
    assert pretty(Transpose(X) + Transpose(Y)) == " T    T\nX  + Y "
    assert pretty(Transpose(X*Y)) == "     T\n(X*Y) "
    assert pretty(Transpose(Y)*Transpose(X)) == " T  T\nY *X "
    assert pretty(Transpose(X**2)) == "    T\n/ 2\\ \n\\X / "
    assert pretty(Transpose(X)**2) == "    2\n/ T\\ \n\\X / "
    assert pretty(Transpose(Inverse(X))) == "     T\n/ -1\\ \n\\X  / "
    assert pretty(Inverse(Transpose(X))) == "    -1\n/ T\\  \n\\X /  "
    assert upretty(Transpose(X)) == " T\nX "
    assert upretty(Transpose(X + Y)) == "       T\n(X + Y) "
    assert upretty(Transpose(X) + Transpose(Y)) == " T    T\nX  + Y "
    assert upretty(Transpose(X*Y)) == "     T\n(X⋅Y) "
    assert upretty(Transpose(Y)*Transpose(X)) == " T  T\nY ⋅X "
    assert upretty(Transpose(X**2)) == \
        "    T\n⎛ 2⎞ \n⎝X ⎠ "
    assert upretty(Transpose(X)**2) == \
        "    2\n⎛ T⎞ \n⎝X ⎠ "
    assert upretty(Transpose(Inverse(X))) == \
        "     T\n⎛ -1⎞ \n⎝X  ⎠ "
    assert upretty(Inverse(Transpose(X))) == \
        "    -1\n⎛ T⎞  \n⎝X ⎠  "
    m = Matrix(((1, 2), (3, 4)))
    assert upretty(Transpose(m)) == \
        '      T\n'\
        '⎡1  2⎤ \n'\
        '⎢    ⎥ \n'\
        '⎣3  4⎦ '
    assert upretty(Transpose(m+X)) == \
        '            T\n'\
        '⎛⎡1  2⎤    ⎞ \n'\
        '⎜⎢    ⎥ + X⎟ \n'\
        '⎝⎣3  4⎦    ⎠ '
    assert upretty(Transpose(BlockMatrix(((OneMatrix(2, 2), X),
                                          (m, ZeroMatrix(2, 2)))))) == \
        '           T\n'\
        '⎡  𝟙     X⎤ \n'\
        '⎢         ⎥ \n'\
        '⎢⎡1  2⎤   ⎥ \n'\
        '⎢⎢    ⎥  𝟘⎥ \n'\
        '⎣⎣3  4⎦   ⎦ '

