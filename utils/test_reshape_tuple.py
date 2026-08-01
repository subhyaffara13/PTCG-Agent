
def test_reshape_tuple():
    a = np.arange(3 * 7 * 2) + 1
    x = m.reshape_tuple(a, (3, 7, 2))
    assert x.shape == (3, 7, 2)
    assert list(x[1][4]) == [23, 24]
    y = m.reshape_tuple(x, (x.size,))
    assert y.shape == (42,)
    with pytest.raises(ValueError) as excinfo:
        m.reshape_tuple(a, (3, 7, 1))
    assert str(excinfo.value) == "cannot reshape array of size 42 into shape (3,7,1)"
    with pytest.raises(ValueError) as excinfo:
        m.reshape_tuple(a, ())
    assert str(excinfo.value) == "cannot reshape array of size 42 into shape ()"

