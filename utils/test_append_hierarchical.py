
def test_append_hierarchical(temp_hdfstore, multiindex_dataframe_random_data):
    df = multiindex_dataframe_random_data
    df.columns.name = None

    temp_hdfstore.append("mi", df)
    result = temp_hdfstore.select("mi")
    tm.assert_frame_equal(result, df)

    # GH 3748
    result = temp_hdfstore.select("mi", columns=["A", "B"])
    expected = df.reindex(columns=["A", "B"])
    tm.assert_frame_equal(result, expected)

    df.to_hdf(temp_hdfstore, key="df", format="table")
    result = read_hdf(temp_hdfstore, "df", columns=["A", "B"])
    expected = df.reindex(columns=["A", "B"])
    tm.assert_frame_equal(result, expected)

