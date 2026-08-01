
def test_setitem_dont_track_unnecessary_references():
    df = DataFrame({"a": [1, 2, 3], "b": 1, "c": 1})

    df["b"] = 100
    arr = get_array(df, "a")
    # We split the block in setitem, if we are not careful the new blocks will
    # reference each other triggering a copy
    df.iloc[0, 0] = 100
    assert np.shares_memory(arr, get_array(df, "a"))

