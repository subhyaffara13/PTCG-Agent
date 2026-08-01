
def test_frame_mi_access_returns_series(dataframe_with_duplicate_index):
    # GH 4146, not returning a block manager when selecting a unique index
    # from a duplicate index
    # as of 4879, this returns a Series (which is similar to what happens
    # with a non-unique)
    df = dataframe_with_duplicate_index
    expected = Series(["a", 1, 1], index=["h1", "h3", "h5"], name="A1")
    result = df["A"]["A1"]
    tm.assert_series_equal(result, expected)

