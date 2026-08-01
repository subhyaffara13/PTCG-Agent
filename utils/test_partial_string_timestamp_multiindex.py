
def test_partial_string_timestamp_multiindex(df):
    # GH10331
    df_swap = df.swaplevel(0, 1).sort_index()
    SLC = IndexSlice

    # indexing with IndexSlice
    result = df.loc[SLC["2016-01-01":"2016-02-01", :], :]
    expected = df
    tm.assert_frame_equal(result, expected)

    # match on secondary index
    result = df_swap.loc[SLC[:, "2016-01-01":"2016-01-01"], :]
    expected = df_swap.iloc[[0, 1, 5, 6, 10, 11]]
    tm.assert_frame_equal(result, expected)

    # partial string match on year only
    result = df.loc["2016"]
    expected = df
    tm.assert_frame_equal(result, expected)

    # partial string match on date
    result = df.loc["2016-01-01"]
    expected = df.iloc[0:6]
    tm.assert_frame_equal(result, expected)

    # partial string match on date and hour, from middle
    result = df.loc["2016-01-02 12"]
    # hourly resolution, same as index.levels[0], so we are _not_ slicing on
    #  that level, so that level gets dropped
    expected = df.iloc[9:12].droplevel(0)
    tm.assert_frame_equal(result, expected)

    # partial string match on secondary index
    result = df_swap.loc[SLC[:, "2016-01-02"], :]
    expected = df_swap.iloc[[2, 3, 7, 8, 12, 13]]
    tm.assert_frame_equal(result, expected)

    # tuple selector with partial string match on date
    # "2016-01-01" has daily resolution, so _is_ a slice on the first level.
    result = df.loc[("2016-01-01", "a"), :]
    expected = df.iloc[[0, 3]]
    expected = df.iloc[[0, 3]].droplevel(1)
    tm.assert_frame_equal(result, expected)

    # Slicing date on first level should break (of course) bc the DTI is the
    #  second level on df_swap
    with pytest.raises(KeyError, match="'2016-01-01'"):
        df_swap.loc["2016-01-01"]

