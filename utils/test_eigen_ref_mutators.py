
def test_eigen_ref_mutators():
    """Tests Eigen's ability to mutate numpy values"""

    orig = np.array([[1.0, 2, 3], [4, 5, 6], [7, 8, 9]])
    zr = np.array(orig)
    zc = np.array(orig, order="F")
    m.add_rm(zr, 1, 0, 100)
    assert np.all(zr == np.array([[1.0, 2, 3], [104, 5, 6], [7, 8, 9]]))
    m.add_cm(zc, 1, 0, 200)
    assert np.all(zc == np.array([[1.0, 2, 3], [204, 5, 6], [7, 8, 9]]))

    m.add_any(zr, 1, 0, 20)
    assert np.all(zr == np.array([[1.0, 2, 3], [124, 5, 6], [7, 8, 9]]))
    m.add_any(zc, 1, 0, 10)
    assert np.all(zc == np.array([[1.0, 2, 3], [214, 5, 6], [7, 8, 9]]))

    # Can't reference a col-major array with a row-major Ref, and vice versa:
    with pytest.raises(TypeError):
        m.add_rm(zc, 1, 0, 1)
    with pytest.raises(TypeError):
        m.add_cm(zr, 1, 0, 1)

    # Overloads:
    m.add1(zr, 1, 0, -100)
    m.add2(zr, 1, 0, -20)
    assert np.all(zr == orig)
    m.add1(zc, 1, 0, -200)
    m.add2(zc, 1, 0, -10)
    assert np.all(zc == orig)

    # a non-contiguous slice (this won't work on either the row- or
    # column-contiguous refs, but should work for the any)
    cornersr = zr[0::2, 0::2]
    cornersc = zc[0::2, 0::2]

    assert np.all(cornersr == np.array([[1.0, 3], [7, 9]]))
    assert np.all(cornersc == np.array([[1.0, 3], [7, 9]]))

    with pytest.raises(TypeError):
        m.add_rm(cornersr, 0, 1, 25)
    with pytest.raises(TypeError):
        m.add_cm(cornersr, 0, 1, 25)
    with pytest.raises(TypeError):
        m.add_rm(cornersc, 0, 1, 25)
    with pytest.raises(TypeError):
        m.add_cm(cornersc, 0, 1, 25)
    m.add_any(cornersr, 0, 1, 25)
    m.add_any(cornersc, 0, 1, 44)
    assert np.all(zr == np.array([[1.0, 2, 28], [4, 5, 6], [7, 8, 9]]))
    assert np.all(zc == np.array([[1.0, 2, 47], [4, 5, 6], [7, 8, 9]]))

    # You shouldn't be allowed to pass a non-writeable array to a mutating Eigen method:
    zro = zr[0:4, 0:4]
    zro.flags.writeable = False
    with pytest.raises(TypeError):
        m.add_rm(zro, 0, 0, 0)
    with pytest.raises(TypeError):
        m.add_any(zro, 0, 0, 0)
    with pytest.raises(TypeError):
        m.add1(zro, 0, 0, 0)
    with pytest.raises(TypeError):
        m.add2(zro, 0, 0, 0)

    # integer array shouldn't be passable to a double-matrix-accepting mutating func:
    zi = np.array([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        m.add_rm(zi)

