
def test_groupby_dataframe_slice_then_transform(dropna, index):
    # GH35014 & GH35612
    expected_data = {"B": [2, 2, 1, np.nan if dropna else 1]}

    df = pd.DataFrame({"A": [0, 0, 1, None], "B": [1, 2, 3, None]}, index=index)
    gb = df.groupby("A", dropna=dropna)

    result = gb.transform(len)
    expected = pd.DataFrame(expected_data, index=index)
    tm.assert_frame_equal(result, expected)

    result = gb[["B"]].transform(len)
    expected = pd.DataFrame(expected_data, index=index)
    tm.assert_frame_equal(result, expected)

    result = gb["B"].transform(len)
    expected = pd.Series(expected_data["B"], index=index, name="B")
    tm.assert_series_equal(result, expected)

