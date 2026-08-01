
def test_array_attributes():
    a = np.array(0, "f8")
    assert m.ndim(a) == 0
    assert all(m.shape(a) == [])
    assert all(m.strides(a) == [])
    with pytest.raises(IndexError) as excinfo:
        m.shape(a, 0)
    assert str(excinfo.value) == "invalid axis: 0 (ndim = 0)"
    with pytest.raises(IndexError) as excinfo:
        m.strides(a, 0)
    assert str(excinfo.value) == "invalid axis: 0 (ndim = 0)"
    assert m.writeable(a)
    assert m.size(a) == 1
    assert m.itemsize(a) == 8
    assert m.nbytes(a) == 8
    assert m.owndata(a)

    a = np.array([[1, 2, 3], [4, 5, 6]], "u2").view()
    a.flags.writeable = False
    assert m.ndim(a) == 2
    assert all(m.shape(a) == [2, 3])
    assert m.shape(a, 0) == 2
    assert m.shape(a, 1) == 3
    assert all(m.strides(a) == [6, 2])
    assert m.strides(a, 0) == 6
    assert m.strides(a, 1) == 2
    with pytest.raises(IndexError) as excinfo:
        m.shape(a, 2)
    assert str(excinfo.value) == "invalid axis: 2 (ndim = 2)"
    with pytest.raises(IndexError) as excinfo:
        m.strides(a, 2)
    assert str(excinfo.value) == "invalid axis: 2 (ndim = 2)"
    assert not m.writeable(a)
    assert m.size(a) == 6
    assert m.itemsize(a) == 2
    assert m.nbytes(a) == 12
    assert not m.owndata(a)

