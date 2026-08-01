
def test_fixed_forward_indexer_bounds(
    window_size, num_values, expected_start, expected_end, step
):
    # GH 43267
    indexer = FixedForwardWindowIndexer(window_size=window_size)
    start, end = indexer.get_window_bounds(num_values=num_values, step=step)

    tm.assert_numpy_array_equal(
        start, np.array(expected_start[::step]), check_dtype=False
    )
    tm.assert_numpy_array_equal(end, np.array(expected_end[::step]), check_dtype=False)
    assert len(start) == len(end)

