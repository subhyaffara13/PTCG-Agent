
def test_eye():
    assert list(SpecialOnlyMatrix.eye(2, 2)) == [1, 0, 0, 1]
    assert list(SpecialOnlyMatrix.eye(2)) == [1, 0, 0, 1]
    assert type(SpecialOnlyMatrix.eye(2)) == SpecialOnlyMatrix
    assert type(SpecialOnlyMatrix.eye(2, cls=Matrix)) == Matrix


def test_eye():
    assert list(Matrix.eye(2, 2)) == [1, 0, 0, 1]
    assert list(Matrix.eye(2)) == [1, 0, 0, 1]
    assert type(Matrix.eye(2)) == Matrix
    assert type(Matrix.eye(2, cls=Matrix)) == Matrix


def test_eye():
    xc = numpy.matlib.eye(3, k=1, dtype=int)
    assert_array_equal(xc, np.matrix([[ 0,  1,  0],
                                      [ 0,  0,  1],
                                      [ 0,  0,  0]]))
    assert xc.flags.c_contiguous
    assert not xc.flags.f_contiguous

    xf = numpy.matlib.eye(3, 4, dtype=int, order='F')
    assert_array_equal(xf, np.matrix([[ 1,  0,  0,  0],
                                      [ 0,  1,  0,  0],
                                      [ 0,  0,  1,  0]]))
    assert not xf.flags.c_contiguous
    assert xf.flags.f_contiguous

