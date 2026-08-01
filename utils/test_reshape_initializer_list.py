
def test_reshape_initializer_list():
    a = np.arange(2 * 7 * 3) + 1
    x = m.reshape_initializer_list(a, 2, 7, 3)
    assert x.shape == (2, 7, 3)
    assert list(x[1][4]) == [34, 35, 36]
    with pytest.raises(ValueError) as excinfo:
        m.reshape_initializer_list(a, 1, 7, 3)
    assert str(excinfo.value) == "cannot reshape array of size 42 into shape (1,7,3)"

