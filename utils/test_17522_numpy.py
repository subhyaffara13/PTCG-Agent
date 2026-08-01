
def test_17522_numpy():
    from sympy.matrices.common import _matrixify
    try:
        from numpy import array, matrix
    except ImportError:
        skip('NumPy must be available to test indexing matrixified NumPy ndarrays and matrices')

    m = _matrixify(array([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]

    with ignore_warnings(PendingDeprecationWarning):
        m = _matrixify(matrix([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]


def test_17522_numpy():
    from sympy.matrices.common import _matrixify
    try:
        from numpy import array, matrix
    except ImportError:
        skip('NumPy must be available to test indexing matrixified NumPy ndarrays and matrices')

    m = _matrixify(array([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]

    with ignore_warnings(PendingDeprecationWarning):
        m = _matrixify(matrix([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]

