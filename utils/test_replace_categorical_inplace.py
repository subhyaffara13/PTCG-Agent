
def test_replace_categorical_inplace():
    df = DataFrame({"a": Categorical([1, 2, 3])})
    arr_a = get_array(df, "a")
    df.replace(to_replace=1, value=1, inplace=True)

    assert np.shares_memory(get_array(df, "a").codes, arr_a.codes)
    assert df._mgr._has_no_reference(0)

    expected = DataFrame({"a": Categorical([1, 2, 3])})
    tm.assert_frame_equal(df, expected)

