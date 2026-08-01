
def test_matrix2numpy_conversion():
    a = Matrix([[1, 2, sin(x)], [x**2, x, Rational(1, 2)]])
    b = array([[1, 2, sin(x)], [x**2, x, Rational(1, 2)]])
    assert (matrix2numpy(a) == b).all()
    assert matrix2numpy(a).dtype == numpy.dtype('object')

    c = matrix2numpy(Matrix([[1, 2], [10, 20]]), dtype='int8')
    d = matrix2numpy(Matrix([[1, 2], [10, 20]]), dtype='float64')
    assert c.dtype == numpy.dtype('int8')
    assert d.dtype == numpy.dtype('float64')

