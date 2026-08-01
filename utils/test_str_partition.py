
def test_str_partition():
    ser = pd.Series(["abcba", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.partition("b")
    expected = pd.DataFrame(
        [["a", "b", "cba"], [None, None, None]],
        dtype=ArrowDtype(pa.string()),
        columns=pd.RangeIndex(3),
    )
    tm.assert_frame_equal(result, expected, check_column_type=True)

    result = ser.str.partition("b", expand=False)
    expected = pd.Series(ArrowExtensionArray(pa.array([["a", "b", "cba"], None])))
    tm.assert_series_equal(result, expected)

    result = ser.str.rpartition("b")
    expected = pd.DataFrame(
        [["abc", "b", "a"], [None, None, None]],
        dtype=ArrowDtype(pa.string()),
        columns=pd.RangeIndex(3),
    )
    tm.assert_frame_equal(result, expected, check_column_type=True)

    result = ser.str.rpartition("b", expand=False)
    expected = pd.Series(ArrowExtensionArray(pa.array([["abc", "b", "a"], None])))
    tm.assert_series_equal(result, expected)

