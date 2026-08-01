
def test_matrix_transpose_raises_error_for_1d():
    msg = "matrix transpose with ndim < 2 is undefined"
    arr = np.arange(48)
    with pytest.raises(ValueError, match=msg):
        arr.mT


def test_matrix_transpose_raises_error_for_1d():
    msg = "matrix transpose with ndim < 2 is undefined"
    ma_arr = masked_array(data=[1, 2, 3, 4, 5, 6],
                          mask=[1, 0, 1, 1, 1, 0])
    with pytest.raises(ValueError, match=msg):
        ma_arr.mT

