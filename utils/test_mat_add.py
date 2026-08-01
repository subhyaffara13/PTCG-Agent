
def test_matAdd():
    C = MatrixSymbol('C', 5, 5)
    B = MatrixSymbol('B', 5, 5)

    n = symbols("n")
    h = MatrixSymbol("h", 1, 1)

    assert latex(C - 2*B) in [r'- 2 B + C', r'C -2 B']
    assert latex(C + 2*B) in [r'2 B + C', r'C + 2 B']
    assert latex(B - 2*C) in [r'B - 2 C', r'- 2 C + B']
    assert latex(B + 2*C) in [r'B + 2 C', r'2 C + B']

    assert latex(n * h - (-h + h.T) * (h + h.T)) == 'n h - \\left(- h + h^{T}\\right) \\left(h + h^{T}\\right)'
    assert latex(MatAdd(MatAdd(h, h), MatAdd(h, h))) == '\\left(h + h\\right) + \\left(h + h\\right)'
    assert latex(MatMul(MatMul(h, h), MatMul(h, h))) == '\\left(h h\\right) \\left(h h\\right)'

