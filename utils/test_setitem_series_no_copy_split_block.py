
def test_setitem_series_no_copy_split_block():
    # Overwriting an existing column that is part of a larger block
    df = DataFrame({"a": [1, 2, 3], "b": 1})
    rhs = Series([4, 5, 6])
    rhs_orig = rhs.copy()

    df["b"] = rhs
    assert np.shares_memory(get_array(rhs), get_array(df, "b"))

    df.iloc[0, 1] = 100
    tm.assert_series_equal(rhs, rhs_orig)

