
def test_select_iterator_multiple(temp_hdfstore):
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    temp_hdfstore.append("df1", df1, data_columns=True)
    df2 = df1.copy().rename(columns="{}_2".format)
    df2["foo"] = "bar"
    temp_hdfstore.append("df2", df2)

    # full selection
    expected = temp_hdfstore.select_as_multiple(["df1", "df2"], selector="df1")
    results = list(
        temp_hdfstore.select_as_multiple(["df1", "df2"], selector="df1", chunksize=2)
    )
    result = concat(results)
    tm.assert_frame_equal(expected, result)

