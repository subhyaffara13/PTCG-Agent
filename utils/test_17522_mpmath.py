
def test_17522_mpmath():
    from sympy.matrices.common import _matrixify
    try:
        from mpmath import matrix
    except ImportError:
        skip('mpmath must be available to test indexing matrixified mpmath matrices')

    m = _matrixify(matrix([[1, 2], [3, 4]]))
    assert m[3] == 4.0
    assert list(m) == [1.0, 2.0, 3.0, 4.0]


def test_17522_mpmath():
    from sympy.matrices.common import _matrixify
    try:
        from mpmath import matrix
    except ImportError:
        skip('mpmath must be available to test indexing matrixified mpmath matrices')

    m = _matrixify(matrix([[1, 2], [3, 4]]))
    assert m[3] == 4.0
    assert list(m) == [1.0, 2.0, 3.0, 4.0]

