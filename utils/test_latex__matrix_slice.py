
def test_latex_MatrixSlice():
    n = Symbol('n', integer=True)
    x, y, z, w, t, = symbols('x y z w t')
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', 10, 10)
    Z = MatrixSymbol('Z', 10, 10)

    assert latex(MatrixSlice(X, (None, None, None), (None, None, None))) == r'X\left[:, :\right]'
    assert latex(X[x:x + 1, y:y + 1]) == r'X\left[x:x + 1, y:y + 1\right]'
    assert latex(X[x:x + 1:2, y:y + 1:2]) == r'X\left[x:x + 1:2, y:y + 1:2\right]'
    assert latex(X[:x, y:]) == r'X\left[:x, y:\right]'
    assert latex(X[:x, y:]) == r'X\left[:x, y:\right]'
    assert latex(X[x:, :y]) == r'X\left[x:, :y\right]'
    assert latex(X[x:y, z:w]) == r'X\left[x:y, z:w\right]'
    assert latex(X[x:y:t, w:t:x]) == r'X\left[x:y:t, w:t:x\right]'
    assert latex(X[x::y, t::w]) == r'X\left[x::y, t::w\right]'
    assert latex(X[:x:y, :t:w]) == r'X\left[:x:y, :t:w\right]'
    assert latex(X[::x, ::y]) == r'X\left[::x, ::y\right]'
    assert latex(MatrixSlice(X, (0, None, None), (0, None, None))) == r'X\left[:, :\right]'
    assert latex(MatrixSlice(X, (None, n, None), (None, n, None))) == r'X\left[:, :\right]'
    assert latex(MatrixSlice(X, (0, n, None), (0, n, None))) == r'X\left[:, :\right]'
    assert latex(MatrixSlice(X, (0, n, 2), (0, n, 2))) == r'X\left[::2, ::2\right]'
    assert latex(X[1:2:3, 4:5:6]) == r'X\left[1:2:3, 4:5:6\right]'
    assert latex(X[1:3:5, 4:6:8]) == r'X\left[1:3:5, 4:6:8\right]'
    assert latex(X[1:10:2]) == r'X\left[1:10:2, :\right]'
    assert latex(Y[:5, 1:9:2]) == r'Y\left[:5, 1:9:2\right]'
    assert latex(Y[:5, 1:10:2]) == r'Y\left[:5, 1::2\right]'
    assert latex(Y[5, :5:2]) == r'Y\left[5:6, :5:2\right]'
    assert latex(X[0:1, 0:1]) == r'X\left[:1, :1\right]'
    assert latex(X[0:1:2, 0:1:2]) == r'X\left[:1:2, :1:2\right]'
    assert latex((Y + Z)[2:, 2:]) == r'\left(Y + Z\right)\left[2:, 2:\right]'

