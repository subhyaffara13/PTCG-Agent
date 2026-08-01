
def test_setitem_with_view_copies():
    df = DataFrame({"a": [1, 2, 3], "b": 1, "c": 1})
    view = df[:]
    expected = df.copy()

    df["b"] = 100
    arr = get_array(df, "a")
    df.iloc[0, 0] = 100  # Check that we correctly track reference
    assert not np.shares_memory(arr, get_array(df, "a"))
    tm.assert_frame_equal(view, expected)

