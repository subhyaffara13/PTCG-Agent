
def test_append_to_multiple_dropna(temp_hdfstore):
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df2 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    ).rename(columns="{}_2".format)
    df1.iloc[1, df1.columns.get_indexer(["A", "B"])] = np.nan
    df = concat([df1, df2], axis=1)

    # dropna=True should guarantee rows are synchronized
    temp_hdfstore.append_to_multiple(
        {"df1": ["A", "B"], "df2": None}, df, selector="df1", dropna=True
    )
    result = temp_hdfstore.select_as_multiple(["df1", "df2"])
    expected = df.dropna()
    tm.assert_frame_equal(result, expected, check_index_type=True)
    tm.assert_index_equal(
        temp_hdfstore.select("df1").index, temp_hdfstore.select("df2").index
    )

