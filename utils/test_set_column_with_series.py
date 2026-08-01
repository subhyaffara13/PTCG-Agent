
def test_set_column_with_series():
    # Case: setting a series as a new column (df[col] = s) copies that data
    # (with delayed copy with CoW)
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    ser = Series([1, 2, 3])

    df["c"] = ser

    assert np.shares_memory(get_array(df, "c"), get_array(ser))

    # and modifying the series does not modify the DataFrame
    ser.iloc[0] = 0
    assert ser.iloc[0] == 0
    tm.assert_series_equal(df["c"], Series([1, 2, 3], name="c"))

