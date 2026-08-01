
def test_groupby_apply_identity_maybecopy_index_identical(func):
    # GH 14927
    # Whether the function returns a copy of the input data or not should not
    # have an impact on the index structure of the result since this is not
    # transparent to the user

    df = DataFrame({"g": [1, 2, 2, 2], "a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})
    result = df.groupby("g", group_keys=False).apply(func)
    tm.assert_frame_equal(result, df[["a", "b"]])

