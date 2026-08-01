
def test_midx_losing_dtype():
    # GH#49830
    midx = MultiIndex.from_arrays([[0, 0], [np.nan, np.nan]])
    midx2 = MultiIndex.from_arrays([[1, 1], [np.nan, np.nan]])
    df1 = DataFrame({"a": [None, 4]}, index=midx)
    df2 = DataFrame({"a": [3, 3]}, index=midx2)
    result = df1.combine_first(df2)
    expected_midx = MultiIndex.from_arrays(
        [[0, 0, 1, 1], [np.nan, np.nan, np.nan, np.nan]]
    )
    expected = DataFrame({"a": [np.nan, 4, 3, 3]}, index=expected_midx)
    tm.assert_frame_equal(result, expected)

