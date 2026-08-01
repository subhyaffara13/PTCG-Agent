
def test_trace():
    # Issue 15303
    from sympy.matrices.expressions.trace import trace
    A = MatrixSymbol("A", 2, 2)
    assert latex(trace(A)) == r"\operatorname{tr}\left(A \right)"
    assert latex(trace(A**2)) == r"\operatorname{tr}\left(A^{2} \right)"


def test_trace():
    M = OperationsOnlyMatrix([[1, 0, 0],
                [0, 5, 0],
                [0, 0, 8]])
    assert M.trace() == 14


def test_trace():
    M = Matrix([[1, 0, 0],
                [0, 5, 0],
                [0, 0, 8]])
    assert M.trace() == 14


def test_trace():
    M = Matrix([[1, 0, 0],
                [0, 5, 0],
                [0, 0, 8]])
    assert M.trace() == 14


def test_trace():
    assert SparseMatrix(((1, 2), (3, 4))).trace() == 5
    assert SparseMatrix(((0, 0), (0, 4))).trace() == 4


def test_trace():
    # Here we only test if selected axes are compatible
    # with Array API (last two). Core implementation
    # of `trace` is tested in `test_multiarray.py`.
    x = np.arange(60).reshape((3, 4, 5))
    actual = np.linalg.trace(x)
    expected = np.array([36, 116, 196])

    assert_equal(actual, expected)

