
def test_partially_fixed():
    ref2 = np.array([[0.0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    np.testing.assert_array_equal(m.partial_copy_four_rm_r(ref2), ref2)
    np.testing.assert_array_equal(m.partial_copy_four_rm_c(ref2), ref2)
    np.testing.assert_array_equal(m.partial_copy_four_rm_r(ref2[:, 1]), ref2[:, [1]])
    np.testing.assert_array_equal(m.partial_copy_four_rm_c(ref2[0, :]), ref2[[0], :])
    np.testing.assert_array_equal(
        m.partial_copy_four_rm_r(ref2[:, (0, 2)]), ref2[:, (0, 2)]
    )
    np.testing.assert_array_equal(
        m.partial_copy_four_rm_c(ref2[(3, 1, 2), :]), ref2[(3, 1, 2), :]
    )

    np.testing.assert_array_equal(m.partial_copy_four_cm_r(ref2), ref2)
    np.testing.assert_array_equal(m.partial_copy_four_cm_c(ref2), ref2)
    np.testing.assert_array_equal(m.partial_copy_four_cm_r(ref2[:, 1]), ref2[:, [1]])
    np.testing.assert_array_equal(m.partial_copy_four_cm_c(ref2[0, :]), ref2[[0], :])
    np.testing.assert_array_equal(
        m.partial_copy_four_cm_r(ref2[:, (0, 2)]), ref2[:, (0, 2)]
    )
    np.testing.assert_array_equal(
        m.partial_copy_four_cm_c(ref2[(3, 1, 2), :]), ref2[(3, 1, 2), :]
    )

    # TypeError should be raise for a shape mismatch
    functions = [
        m.partial_copy_four_rm_r,
        m.partial_copy_four_rm_c,
        m.partial_copy_four_cm_r,
        m.partial_copy_four_cm_c,
    ]
    matrix_with_wrong_shape = [[1, 2], [3, 4]]
    for f in functions:
        with pytest.raises(TypeError) as excinfo:
            f(matrix_with_wrong_shape)
        assert "incompatible function arguments" in str(excinfo.value)

