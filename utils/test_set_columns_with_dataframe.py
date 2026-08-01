
def test_set_columns_with_dataframe():
    # Case: setting a DataFrame as new columns copies that data
    # (with delayed copy with CoW)
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df2 = DataFrame({"c": [7, 8, 9], "d": [10, 11, 12]})

    df[["c", "d"]] = df2

    assert np.shares_memory(get_array(df, "c"), get_array(df2, "c"))
    # and modifying the set DataFrame does not modify the original DataFrame
    df2.iloc[0, 0] = 0
    tm.assert_series_equal(df["c"], Series([7, 8, 9], name="c"))

