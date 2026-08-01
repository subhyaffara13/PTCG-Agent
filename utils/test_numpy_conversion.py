
def test_numpy_conversion():
    try:
        from numpy import array, array_equal
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')
    A = Matrix([[1,2], [3,4]])
    np_array = array([[1,2], [3,4]])
    assert array_equal(array(A), np_array)
    assert array_equal(array(A, copy=True), np_array)
    if(int(version('numpy').split('.')[0]) >= 2): #run this test only if numpy is new enough that copy variable is passed properly.
        raises(TypeError, lambda: array(A, copy=False))


def test_numpy_conversion():
    try:
        from numpy import array, array_equal
    except ImportError:
        skip('NumPy must be available to test creating matrices from ndarrays')
    A = MatrixSymbol('A', 2, 2)
    np_array = array([[MatrixElement(A, 0, 0), MatrixElement(A, 0, 1)],
    [MatrixElement(A, 1, 0), MatrixElement(A, 1, 1)]])
    assert array_equal(array(A), np_array)
    assert array_equal(array(A, copy=True), np_array)
    if(int(version('numpy').split('.')[0]) >= 2): #run this test only if numpy is new enough that copy variable is passed properly.
        raises(TypeError, lambda: array(A, copy=False))

