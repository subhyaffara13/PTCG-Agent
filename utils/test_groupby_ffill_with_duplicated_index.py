
def test_groupby_ffill_with_duplicated_index():
    # GH#43412
    df = DataFrame({"a": [1, 2, 3, 4, np.nan, np.nan]}, index=[0, 1, 2, 0, 1, 2])

    result = df.groupby(level=0).ffill()
    expected = DataFrame({"a": [1, 2, 3, 4, 2, 3]}, index=[0, 1, 2, 0, 1, 2])
    tm.assert_frame_equal(result, expected, check_dtype=False)

