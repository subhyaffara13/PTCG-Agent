
def test_infer_objects(using_infer_string):
    df = DataFrame(
        {"a": [1, 2], "b": Series(["x", "y"], dtype=object), "c": 1, "d": "x"}
    )
    df_orig = df.copy()
    df2 = df.infer_objects()

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    if using_infer_string and HAS_PYARROW:
        assert not tm.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    else:
        assert np.shares_memory(get_array(df2, "b"), get_array(df, "b"))

    df2.iloc[0, 0] = 0
    df2.iloc[0, 1] = "d"
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert not np.shares_memory(get_array(df2, "b"), get_array(df, "b"))
    tm.assert_frame_equal(df, df_orig)


def test_infer_objects(idx):
    with pytest.raises(NotImplementedError, match="to_frame"):
        idx.infer_objects()


def test_infer_objects():
    idx, view_ = index_view(["a", "b"])
    expected = idx.copy(deep=True)
    idx = idx.infer_objects(copy=False)
    view_.iloc[0, 0] = "aaaa"
    tm.assert_index_equal(idx, expected, check_names=False)

