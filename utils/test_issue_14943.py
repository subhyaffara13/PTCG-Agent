
def test_issue_14943():
    # Test that __array__ accepts the optional dtype argument
    try:
        from numpy import array
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')

    M = Matrix([[1,2], [3,4]])
    assert array(M, dtype=float).dtype.name == 'float64'


def test_issue_14943():
    # Test that __array__ accepts the optional dtype argument
    try:
        from numpy import array
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')

    M = Matrix([[1,2], [3,4]])
    assert array(M, dtype=float).dtype.name == 'float64'

