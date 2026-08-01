
def test_nonunit_stride_from_python():
    counting_mat = np.arange(9.0, dtype=np.float32).reshape((3, 3))
    second_row = counting_mat[1, :]
    second_col = counting_mat[:, 1]
    np.testing.assert_array_equal(m.double_row(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_col(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_complex(second_row), 2.0 * second_row)
    np.testing.assert_array_equal(m.double_row(second_col), 2.0 * second_col)
    np.testing.assert_array_equal(m.double_col(second_col), 2.0 * second_col)
    np.testing.assert_array_equal(m.double_complex(second_col), 2.0 * second_col)

    counting_3d = np.arange(27.0, dtype=np.float32).reshape((3, 3, 3))
    slices = [counting_3d[0, :, :], counting_3d[:, 0, :], counting_3d[:, :, 0]]
    for ref_mat in slices:
        np.testing.assert_array_equal(m.double_mat_cm(ref_mat), 2.0 * ref_mat)
        np.testing.assert_array_equal(m.double_mat_rm(ref_mat), 2.0 * ref_mat)

    # Mutator:
    m.double_threer(second_row)
    m.double_threec(second_col)
    np.testing.assert_array_equal(counting_mat, [[0.0, 2, 2], [6, 16, 10], [6, 14, 8]])

