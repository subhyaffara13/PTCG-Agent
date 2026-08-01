
def test_Hadamard():
    from sympy.matrices import HadamardProduct, HadamardPower
    from sympy.matrices.expressions import MatAdd, MatMul, MatPow
    X = MatrixSymbol('X', 2, 2)
    Y = MatrixSymbol('Y', 2, 2)
    assert latex(HadamardProduct(X, Y*Y)) == r'X \circ Y^{2}'
    assert latex(HadamardProduct(X, Y)*Y) == r'\left(X \circ Y\right) Y'

    assert latex(HadamardPower(X, 2)) == r'X^{\circ {2}}'
    assert latex(HadamardPower(X, -1)) == r'X^{\circ \left({-1}\right)}'
    assert latex(HadamardPower(MatAdd(X, Y), 2)) == \
        r'\left(X + Y\right)^{\circ {2}}'
    assert latex(HadamardPower(MatMul(X, Y), 2)) == \
        r'\left(X Y\right)^{\circ {2}}'

    assert latex(HadamardPower(MatPow(X, -1), -1)) == \
        r'\left(X^{-1}\right)^{\circ \left({-1}\right)}'
    assert latex(MatPow(HadamardPower(X, -1), -1)) == \
        r'\left(X^{\circ \left({-1}\right)}\right)^{-1}'

    assert latex(HadamardPower(X, n+1)) == \
        r'X^{\circ \left({n + 1}\right)}'

