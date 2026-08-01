
def test_matrix_transpose_equals_transpose_2d():
    arr = np.arange(48).reshape((6, 8))
    assert_array_equal(arr.T, arr.mT)


def test_matrix_transpose_equals_transpose_2d():
    ma_arr = masked_array(data=[[1, 2, 3], [4, 5, 6]],
                          mask=[[1, 0, 1], [1, 1, 0]])
    assert_array_equal(ma_arr.T, ma_arr.mT)

