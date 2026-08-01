
def test_zeros():
    assert list(SpecialOnlyMatrix.zeros(2, 2)) == [0, 0, 0, 0]
    assert list(SpecialOnlyMatrix.zeros(2)) == [0, 0, 0, 0]
    assert SpecialOnlyMatrix.zeros(2, 3) == Matrix([[0, 0, 0], [0, 0, 0]])
    assert type(SpecialOnlyMatrix.zeros(2)) == SpecialOnlyMatrix
    assert type(SpecialOnlyMatrix.zeros(2, cls=Matrix)) == Matrix


def test_zeros():
    assert list(Matrix.zeros(2, 2)) == [0, 0, 0, 0]
    assert list(Matrix.zeros(2)) == [0, 0, 0, 0]
    assert Matrix.zeros(2, 3) == Matrix([[0, 0, 0], [0, 0, 0]])
    assert type(Matrix.zeros(2)) == Matrix
    assert type(Matrix.zeros(2, cls=Matrix)) == Matrix


def test_zeros():
    assert_array_equal(numpy.matlib.zeros((2, 3)),
                       np.matrix([[ 0.,  0.,  0.],
                                  [ 0.,  0.,  0.]]))

    assert_array_equal(numpy.matlib.zeros(2), np.matrix([[0.,  0.]]))

