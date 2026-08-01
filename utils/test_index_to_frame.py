
def test_index_to_frame():
    idx = Index([1, 2, 3], name="a")
    expected = idx.copy(deep=True)
    df = idx.to_frame()
    assert np.shares_memory(get_array(df, "a"), idx._values)
    assert not df._mgr._has_no_reference(0)

    df.iloc[0, 0] = 100
    tm.assert_index_equal(idx, expected)

