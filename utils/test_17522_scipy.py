
def test_17522_scipy():
    from sympy.matrices.common import _matrixify
    try:
        from scipy.sparse import csr_matrix
    except ImportError:
        skip('SciPy must be available to test indexing matrixified SciPy sparse matrices')

    m = _matrixify(csr_matrix([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]


def test_17522_scipy():
    from sympy.matrices.common import _matrixify
    try:
        from scipy.sparse import csr_matrix
    except ImportError:
        skip('SciPy must be available to test indexing matrixified SciPy sparse matrices')

    m = _matrixify(csr_matrix([[1, 2], [3, 4]]))
    assert m[3] == 4
    assert list(m) == [1, 2, 3, 4]

