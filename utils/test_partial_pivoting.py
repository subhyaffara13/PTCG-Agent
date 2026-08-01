
def test_partial_pivoting():
    # example from https://en.wikipedia.org/wiki/Pivot_element
    # partial pivoting with back substitution gives a perfect result
    # naive pivoting give an error ~1e-13, so anything better than
    # 1e-15 is good
    mm=Matrix([[0.003, 59.14, 59.17], [5.291, -6.13, 46.78]])
    assert (mm.rref()[0] - Matrix([[1.0,   0, 10.0],
                                   [  0, 1.0,  1.0]])).norm() < 1e-15

    # issue #11549
    m_mixed = Matrix([[6e-17, 1.0, 4],
                      [ -1.0,   0, 8],
                      [    0,   0, 1]])
    m_float = Matrix([[6e-17,  1.0, 4.],
                      [ -1.0,   0., 8.],
                      [   0.,   0., 1.]])
    m_inv = Matrix([[  0,    -1.0,  8.0],
                    [1.0, 6.0e-17, -4.0],
                    [  0,       0,    1]])
    # this example is numerically unstable and involves a matrix with a norm >= 8,
    # this comparing the difference of the results with 1e-15 is numerically sound.
    assert (m_mixed.inv() - m_inv).norm() < 1e-15
    assert (m_float.inv() - m_inv).norm() < 1e-15


def test_partial_pivoting():
    # example from https://en.wikipedia.org/wiki/Pivot_element
    # partial pivoting with back substitution gives a perfect result
    # naive pivoting give an error ~1e-13, so anything better than
    # 1e-15 is good
    mm=Matrix([[0.003, 59.14, 59.17], [5.291, -6.13, 46.78]])
    assert (mm.rref()[0] - Matrix([[1.0,   0, 10.0],
                                   [  0, 1.0,  1.0]])).norm() < 1e-15

    # issue #11549
    m_mixed = Matrix([[6e-17, 1.0, 4],
                      [ -1.0,   0, 8],
                      [    0,   0, 1]])
    m_float = Matrix([[6e-17,  1.0, 4.],
                      [ -1.0,   0., 8.],
                      [   0.,   0., 1.]])
    m_inv = Matrix([[  0,    -1.0,  8.0],
                    [1.0, 6.0e-17, -4.0],
                    [  0,       0,    1]])
    # this example is numerically unstable and involves a matrix with a norm >= 8,
    # this comparing the difference of the results with 1e-15 is numerically sound.
    assert (m_mixed.inv() - m_inv).norm() < 1e-15
    assert (m_float.inv() - m_inv).norm() < 1e-15

