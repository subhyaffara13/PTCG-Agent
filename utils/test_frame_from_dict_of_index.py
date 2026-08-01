
def test_frame_from_dict_of_index():
    idx = Index([1, 2, 3])
    expected = idx.copy(deep=True)
    df = DataFrame({"a": idx}, copy=False)
    assert np.shares_memory(get_array(df, "a"), idx._values)
    assert not df._mgr._has_no_reference(0)

    df.iloc[0, 0] = 100
    tm.assert_index_equal(idx, expected)

