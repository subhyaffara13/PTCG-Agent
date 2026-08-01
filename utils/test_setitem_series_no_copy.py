
def test_setitem_series_no_copy():
    # Case: setting a Series as column into a DataFrame can delay copying that data
    df = DataFrame({"a": [1, 2, 3]})
    rhs = Series([4, 5, 6])
    rhs_orig = rhs.copy()

    # adding a new column
    df["b"] = rhs
    assert np.shares_memory(get_array(rhs), get_array(df, "b"))

    df.iloc[0, 1] = 100
    tm.assert_series_equal(rhs, rhs_orig)

