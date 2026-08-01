
def test_ones():
    assert list(SpecialOnlyMatrix.ones(2, 2)) == [1, 1, 1, 1]
    assert list(SpecialOnlyMatrix.ones(2)) == [1, 1, 1, 1]
    assert SpecialOnlyMatrix.ones(2, 3) == Matrix([[1, 1, 1], [1, 1, 1]])
    assert type(SpecialOnlyMatrix.ones(2)) == SpecialOnlyMatrix
    assert type(SpecialOnlyMatrix.ones(2, cls=Matrix)) == Matrix


def test_ones():
    assert list(Matrix.ones(2, 2)) == [1, 1, 1, 1]
    assert list(Matrix.ones(2)) == [1, 1, 1, 1]
    assert Matrix.ones(2, 3) == Matrix([[1, 1, 1], [1, 1, 1]])
    assert type(Matrix.ones(2)) == Matrix
    assert type(Matrix.ones(2, cls=Matrix)) == Matrix


def test_ones():
    assert_array_equal(numpy.matlib.ones((2, 3)),
                       np.matrix([[ 1.,  1.,  1.],
                                  [ 1.,  1.,  1.]]))

    assert_array_equal(numpy.matlib.ones(2), np.matrix([[ 1.,  1.]]))

