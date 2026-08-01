
def test_mix(slice_test_df, slice_test_grouped):
    # Test mixed tuple of ints and slices
    result = slice_test_grouped._positional_selector[0, 1, -2:]
    expected = slice_test_df.iloc[[0, 1, 2, 3, 4, 6, 7]]

    tm.assert_frame_equal(result, expected)

