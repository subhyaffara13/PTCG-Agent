
def test_from_ndarray():
    """See issue 7465."""
    try:
        from numpy import array
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')

    assert Matrix(array([1, 2, 3])) == Matrix([1, 2, 3])
    assert Matrix(array([[1, 2, 3]])) == Matrix([[1, 2, 3]])
    assert Matrix(array([[1, 2, 3], [4, 5, 6]])) == \
        Matrix([[1, 2, 3], [4, 5, 6]])
    assert Matrix(array([x, y, z])) == Matrix([x, y, z])
    raises(NotImplementedError,
        lambda: Matrix(array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])))
    assert Matrix([array([1, 2]), array([3, 4])]) == Matrix([[1, 2], [3, 4]])
    assert Matrix([array([1, 2]), [3, 4]]) == Matrix([[1, 2], [3, 4]])
    assert Matrix([array([]), array([])]) == Matrix(2, 0, []) != Matrix(0, 0, [])


def test_from_ndarray():
    """See issue 7465."""
    try:
        from numpy import array
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')

    assert Matrix(array([1, 2, 3])) == Matrix([1, 2, 3])
    assert Matrix(array([[1, 2, 3]])) == Matrix([[1, 2, 3]])
    assert Matrix(array([[1, 2, 3], [4, 5, 6]])) == \
        Matrix([[1, 2, 3], [4, 5, 6]])
    assert Matrix(array([x, y, z])) == Matrix([x, y, z])
    raises(NotImplementedError,
        lambda: Matrix(array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])))
    assert Matrix([array([1, 2]), array([3, 4])]) == Matrix([[1, 2], [3, 4]])
    assert Matrix([array([1, 2]), [3, 4]]) == Matrix([[1, 2], [3, 4]])
    assert Matrix([array([]), array([])]) == Matrix(2, 0, []) != Matrix([])

