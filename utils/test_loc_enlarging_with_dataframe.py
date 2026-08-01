
def test_loc_enlarging_with_dataframe():
    df = DataFrame({"a": [1, 2, 3]})
    rhs = DataFrame({"b": [1, 2, 3], "c": [4, 5, 6]})
    rhs_orig = rhs.copy()
    df.loc[:, ["b", "c"]] = rhs
    assert np.shares_memory(get_array(df, "b"), get_array(rhs, "b"))
    assert np.shares_memory(get_array(df, "c"), get_array(rhs, "c"))
    assert not df._mgr._has_no_reference(1)

    df.iloc[0, 1] = 100
    tm.assert_frame_equal(rhs, rhs_orig)

