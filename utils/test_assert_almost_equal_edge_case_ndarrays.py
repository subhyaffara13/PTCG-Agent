
def test_assert_almost_equal_edge_case_ndarrays(left_dtype, right_dtype):
    # Empty compare.
    _assert_almost_equal_both(
        np.array([], dtype=left_dtype),
        np.array([], dtype=right_dtype),
        check_dtype=False,
    )

