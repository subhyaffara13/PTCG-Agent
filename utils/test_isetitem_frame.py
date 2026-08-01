
def test_isetitem_frame():
    df = DataFrame({"a": [1, 2, 3], "b": 1, "c": 2})
    rhs = DataFrame({"a": [4, 5, 6], "b": 2})
    df.isetitem([0, 1], rhs)
    assert np.shares_memory(get_array(df, "a"), get_array(rhs, "a"))
    assert np.shares_memory(get_array(df, "b"), get_array(rhs, "b"))
    assert not df._mgr._has_no_reference(0)
    expected = df.copy()
    rhs.iloc[0, 0] = 100
    rhs.iloc[0, 1] = 100
    tm.assert_frame_equal(df, expected)

