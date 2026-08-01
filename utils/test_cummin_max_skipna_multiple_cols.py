
def test_cummin_max_skipna_multiple_cols(method):
    # Ensure missing value in "a" doesn't cause "b" to be nan-filled
    df = DataFrame({"a": [np.nan, 2.0, 2.0], "b": [2.0, 2.0, 2.0]})
    gb = df.groupby([1, 1, 1])[["a", "b"]]

    result = getattr(gb, method)(skipna=False)
    expected = DataFrame({"a": [np.nan, np.nan, np.nan], "b": [2.0, 2.0, 2.0]})

    tm.assert_frame_equal(result, expected)

