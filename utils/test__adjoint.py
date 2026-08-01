
def test_Adjoint():
    from sympy.matrices import Adjoint, Inverse, Transpose
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert latex(Adjoint(X)) == r'X^{\dagger}'
    assert latex(Adjoint(X + Y)) == r'\left(X + Y\right)^{\dagger}'
    assert latex(Adjoint(X) + Adjoint(Y)) == r'X^{\dagger} + Y^{\dagger}'
    assert latex(Adjoint(X*Y)) == r'\left(X Y\right)^{\dagger}'
    assert latex(Adjoint(Y)*Adjoint(X)) == r'Y^{\dagger} X^{\dagger}'
    assert latex(Adjoint(X**2)) == r'\left(X^{2}\right)^{\dagger}'
    assert latex(Adjoint(X)**2) == r'\left(X^{\dagger}\right)^{2}'
    assert latex(Adjoint(Inverse(X))) == r'\left(X^{-1}\right)^{\dagger}'
    assert latex(Inverse(Adjoint(X))) == r'\left(X^{\dagger}\right)^{-1}'
    assert latex(Adjoint(Transpose(X))) == r'\left(X^{T}\right)^{\dagger}'
    assert latex(Transpose(Adjoint(X))) == r'\left(X^{\dagger}\right)^{T}'
    assert latex(Transpose(Adjoint(X) + Y)) == r'\left(X^{\dagger} + Y\right)^{T}'
    m = Matrix(((1, 2), (3, 4)))
    assert latex(Adjoint(m)) == '\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right]^{\\dagger}'
    assert latex(Adjoint(m+X)) == \
        '\\left(\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] + X\\right)^{\\dagger}'
    from sympy.matrices import BlockMatrix, OneMatrix, ZeroMatrix
    assert latex(Adjoint(BlockMatrix(((OneMatrix(2, 2), X),
                                      (m, ZeroMatrix(2, 2)))))) == \
        '\\left[\\begin{matrix}1 & X\\\\\\left[\\begin{matrix}1 & 2\\\\3 & 4\\end{matrix}\\right] & 0\\end{matrix}\\right]^{\\dagger}'
    # Issue 20959
    Mx = MatrixSymbol('M^x', 2, 2)
    assert latex(Adjoint(Mx)) == r'\left(M^{x}\right)^{\dagger}'

    # adjoint style
    assert latex(Adjoint(X), adjoint_style="star") == r'X^{\ast}'
    assert latex(Adjoint(X + Y), adjoint_style="hermitian") == r'\left(X + Y\right)^{\mathsf{H}}'
    assert latex(Adjoint(X) + Adjoint(Y), adjoint_style="dagger") == r'X^{\dagger} + Y^{\dagger}'
    assert latex(Adjoint(Y)*Adjoint(X)) == r'Y^{\dagger} X^{\dagger}'
    assert latex(Adjoint(X**2), adjoint_style="star") == r'\left(X^{2}\right)^{\ast}'
    assert latex(Adjoint(X)**2, adjoint_style="hermitian") == r'\left(X^{\mathsf{H}}\right)^{2}'


def test_Adjoint():
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert pretty(Adjoint(X)) == " +\nX "
    assert pretty(Adjoint(X + Y)) == "       +\n(X + Y) "
    assert pretty(Adjoint(X) + Adjoint(Y)) == " +    +\nX  + Y "
    assert pretty(Adjoint(X*Y)) == "     +\n(X*Y) "
    assert pretty(Adjoint(Y)*Adjoint(X)) == " +  +\nY *X "
    assert pretty(Adjoint(X**2)) == "    +\n/ 2\\ \n\\X / "
    assert pretty(Adjoint(X)**2) == "    2\n/ +\\ \n\\X / "
    assert pretty(Adjoint(Inverse(X))) == "     +\n/ -1\\ \n\\X  / "
    assert pretty(Inverse(Adjoint(X))) == "    -1\n/ +\\  \n\\X /  "
    assert pretty(Adjoint(Transpose(X))) == "    +\n/ T\\ \n\\X / "
    assert pretty(Transpose(Adjoint(X))) == "    T\n/ +\\ \n\\X / "
    assert upretty(Adjoint(X)) == " †\nX "
    assert upretty(Adjoint(X + Y)) == "       †\n(X + Y) "
    assert upretty(Adjoint(X) + Adjoint(Y)) == " †    †\nX  + Y "
    assert upretty(Adjoint(X*Y)) == "     †\n(X⋅Y) "
    assert upretty(Adjoint(Y)*Adjoint(X)) == " †  †\nY ⋅X "
    assert upretty(Adjoint(X**2)) == \
        "    †\n⎛ 2⎞ \n⎝X ⎠ "
    assert upretty(Adjoint(X)**2) == \
        "    2\n⎛ †⎞ \n⎝X ⎠ "
    assert upretty(Adjoint(Inverse(X))) == \
        "     †\n⎛ -1⎞ \n⎝X  ⎠ "
    assert upretty(Inverse(Adjoint(X))) == \
        "    -1\n⎛ †⎞  \n⎝X ⎠  "
    assert upretty(Adjoint(Transpose(X))) == \
        "    †\n⎛ T⎞ \n⎝X ⎠ "
    assert upretty(Transpose(Adjoint(X))) == \
        "    T\n⎛ †⎞ \n⎝X ⎠ "
    m = Matrix(((1, 2), (3, 4)))
    assert upretty(Adjoint(m)) == \
        '      †\n'\
        '⎡1  2⎤ \n'\
        '⎢    ⎥ \n'\
        '⎣3  4⎦ '
    assert upretty(Adjoint(m+X)) == \
        '            †\n'\
        '⎛⎡1  2⎤    ⎞ \n'\
        '⎜⎢    ⎥ + X⎟ \n'\
        '⎝⎣3  4⎦    ⎠ '
    assert upretty(Adjoint(BlockMatrix(((OneMatrix(2, 2), X),
                                        (m, ZeroMatrix(2, 2)))))) == \
        '           †\n'\
        '⎡  𝟙     X⎤ \n'\
        '⎢         ⎥ \n'\
        '⎢⎡1  2⎤   ⎥ \n'\
        '⎢⎢    ⎥  𝟘⎥ \n'\
        '⎣⎣3  4⎦   ⎦ '

