
def test_MatrixSlice():
    cache = {}

    n = sy.Symbol('n', integer=True)
    X = sy.MatrixSymbol('X', n, n)

    Y = X[1:2:3, 4:5:6]
    Yt = aesara_code_(Y, cache=cache)

    s = ScalarType('int64')
    assert tuple(Yt.owner.op.idx_list) == (slice(s, s, s), slice(s, s, s))
    assert Yt.owner.inputs[0] == aesara_code_(X, cache=cache)
    # == doesn't work in Aesara like it does in SymPy. You have to use
    # equals.
    assert all(Yt.owner.inputs[i].data == i for i in range(1, 7))

    k = sy.Symbol('k')
    aesara_code_(k, dtypes={k: 'int32'})
    start, stop, step = 4, k, 2
    Y = X[start:stop:step]
    Yt = aesara_code_(Y, dtypes={n: 'int32', k: 'int32'})


def test_MatrixSlice():
    n = Symbol('n', integer=True)
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', 10, 10)
    Z = MatrixSymbol('Z', 10, 10)

    assert str(MatrixSlice(X, (None, None, None), (None, None, None))) == 'X[:, :]'
    assert str(X[x:x + 1, y:y + 1]) == 'X[x:x + 1, y:y + 1]'
    assert str(X[x:x + 1:2, y:y + 1:2]) == 'X[x:x + 1:2, y:y + 1:2]'
    assert str(X[:x, y:]) == 'X[:x, y:]'
    assert str(X[:x, y:]) == 'X[:x, y:]'
    assert str(X[x:, :y]) == 'X[x:, :y]'
    assert str(X[x:y, z:w]) == 'X[x:y, z:w]'
    assert str(X[x:y:t, w:t:x]) == 'X[x:y:t, w:t:x]'
    assert str(X[x::y, t::w]) == 'X[x::y, t::w]'
    assert str(X[:x:y, :t:w]) == 'X[:x:y, :t:w]'
    assert str(X[::x, ::y]) == 'X[::x, ::y]'
    assert str(MatrixSlice(X, (0, None, None), (0, None, None))) == 'X[:, :]'
    assert str(MatrixSlice(X, (None, n, None), (None, n, None))) == 'X[:, :]'
    assert str(MatrixSlice(X, (0, n, None), (0, n, None))) == 'X[:, :]'
    assert str(MatrixSlice(X, (0, n, 2), (0, n, 2))) == 'X[::2, ::2]'
    assert str(X[1:2:3, 4:5:6]) == 'X[1:2:3, 4:5:6]'
    assert str(X[1:3:5, 4:6:8]) == 'X[1:3:5, 4:6:8]'
    assert str(X[1:10:2]) == 'X[1:10:2, :]'
    assert str(Y[:5, 1:9:2]) == 'Y[:5, 1:9:2]'
    assert str(Y[:5, 1:10:2]) == 'Y[:5, 1::2]'
    assert str(Y[5, :5:2]) == 'Y[5:6, :5:2]'
    assert str(X[0:1, 0:1]) == 'X[:1, :1]'
    assert str(X[0:1:2, 0:1:2]) == 'X[:1:2, :1:2]'
    assert str((Y + Z)[2:, 2:]) == '(Y + Z)[2:, 2:]'


def test_MatrixSlice():
    from theano import Constant

    cache = {}

    n = sy.Symbol('n', integer=True)
    X = sy.MatrixSymbol('X', n, n)

    Y = X[1:2:3, 4:5:6]
    Yt = theano_code_(Y, cache=cache)

    s = ts.Scalar('int64')
    assert tuple(Yt.owner.op.idx_list) == (slice(s, s, s), slice(s, s, s))
    assert Yt.owner.inputs[0] == theano_code_(X, cache=cache)
    # == doesn't work in theano like it does in SymPy. You have to use
    # equals.
    assert all(Yt.owner.inputs[i].equals(Constant(s, i)) for i in range(1, 7))

    k = sy.Symbol('k')
    theano_code_(k, dtypes={k: 'int32'})
    start, stop, step = 4, k, 2
    Y = X[start:stop:step]
    Yt = theano_code_(Y, dtypes={n: 'int32', k: 'int32'})


def test_MatrixSlice():
    n = Symbol('n', integer=True)
    x, y, z, w, t, = symbols('x y z w t')
    X = MatrixSymbol('X', n, n)
    Y = MatrixSymbol('Y', 10, 10)
    Z = MatrixSymbol('Z', 10, 10)

    expr = MatrixSlice(X, (None, None, None), (None, None, None))
    assert pretty(expr) == upretty(expr) == 'X[:, :]'
    expr = X[x:x + 1, y:y + 1]
    assert pretty(expr) == upretty(expr) == 'X[x:x + 1, y:y + 1]'
    expr = X[x:x + 1:2, y:y + 1:2]
    assert pretty(expr) == upretty(expr) == 'X[x:x + 1:2, y:y + 1:2]'
    expr = X[:x, y:]
    assert pretty(expr) == upretty(expr) == 'X[:x, y:]'
    expr = X[:x, y:]
    assert pretty(expr) == upretty(expr) == 'X[:x, y:]'
    expr = X[x:, :y]
    assert pretty(expr) == upretty(expr) == 'X[x:, :y]'
    expr = X[x:y, z:w]
    assert pretty(expr) == upretty(expr) == 'X[x:y, z:w]'
    expr = X[x:y:t, w:t:x]
    assert pretty(expr) == upretty(expr) == 'X[x:y:t, w:t:x]'
    expr = X[x::y, t::w]
    assert pretty(expr) == upretty(expr) == 'X[x::y, t::w]'
    expr = X[:x:y, :t:w]
    assert pretty(expr) == upretty(expr) == 'X[:x:y, :t:w]'
    expr = X[::x, ::y]
    assert pretty(expr) == upretty(expr) == 'X[::x, ::y]'
    expr = MatrixSlice(X, (0, None, None), (0, None, None))
    assert pretty(expr) == upretty(expr) == 'X[:, :]'
    expr = MatrixSlice(X, (None, n, None), (None, n, None))
    assert pretty(expr) == upretty(expr) == 'X[:, :]'
    expr = MatrixSlice(X, (0, n, None), (0, n, None))
    assert pretty(expr) == upretty(expr) == 'X[:, :]'
    expr = MatrixSlice(X, (0, n, 2), (0, n, 2))
    assert pretty(expr) == upretty(expr) == 'X[::2, ::2]'
    expr = X[1:2:3, 4:5:6]
    assert pretty(expr) == upretty(expr) == 'X[1:2:3, 4:5:6]'
    expr = X[1:3:5, 4:6:8]
    assert pretty(expr) == upretty(expr) == 'X[1:3:5, 4:6:8]'
    expr = X[1:10:2]
    assert pretty(expr) == upretty(expr) == 'X[1:10:2, :]'
    expr = Y[:5, 1:9:2]
    assert pretty(expr) == upretty(expr) == 'Y[:5, 1:9:2]'
    expr = Y[:5, 1:10:2]
    assert pretty(expr) == upretty(expr) == 'Y[:5, 1::2]'
    expr = Y[5, :5:2]
    assert pretty(expr) == upretty(expr) == 'Y[5:6, :5:2]'
    expr = X[0:1, 0:1]
    assert pretty(expr) == upretty(expr) == 'X[:1, :1]'
    expr = X[0:1:2, 0:1:2]
    assert pretty(expr) == upretty(expr) == 'X[:1:2, :1:2]'
    expr = (Y + Z)[2:, 2:]
    assert pretty(expr) == upretty(expr) == '(Y + Z)[2:, 2:]'


def test_MatrixSlice():
    X = MatrixSymbol('X', 4, 4)
    B = MatrixSlice(X, (1, 3), (1, 3))
    C = MatrixSlice(X, (0, 3), (1, 3))
    assert ask(Q.symmetric(B), Q.symmetric(X))
    assert ask(Q.invertible(B), Q.invertible(X))
    assert ask(Q.diagonal(B), Q.diagonal(X))
    assert ask(Q.orthogonal(B), Q.orthogonal(X))
    assert ask(Q.upper_triangular(B), Q.upper_triangular(X))

    assert not ask(Q.symmetric(C), Q.symmetric(X))
    assert not ask(Q.invertible(C), Q.invertible(X))
    assert not ask(Q.diagonal(C), Q.diagonal(X))
    assert not ask(Q.orthogonal(C), Q.orthogonal(X))
    assert not ask(Q.upper_triangular(C), Q.upper_triangular(X))

