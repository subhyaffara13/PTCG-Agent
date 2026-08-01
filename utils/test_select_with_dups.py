
def test_select_with_dups(temp_hdfstore):
    # single dtypes
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)), columns=["A", "A", "B", "B"]
    )
    df.index = date_range("20130101 9:30", periods=10, freq="min", unit="ns")

    temp_hdfstore.append("df", df)

    result = temp_hdfstore.select("df")
    expected = df
    tm.assert_frame_equal(result, expected, by_blocks=True)

    result = temp_hdfstore.select("df", columns=df.columns)
    expected = df
    tm.assert_frame_equal(result, expected, by_blocks=True)

    result = temp_hdfstore.select("df", columns=["A"])
    expected = df.loc[:, ["A"]]
    tm.assert_frame_equal(result, expected)

