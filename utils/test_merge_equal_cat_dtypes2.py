
def test_merge_equal_cat_dtypes2():
    # see gh-22501
    cat_dtype = CategoricalDtype(categories=["a", "b", "c"], ordered=False)

    # Test Data
    df1 = DataFrame(
        {"foo": Series(["a", "b"]).astype(cat_dtype), "left": [1, 2]}
    ).set_index("foo")

    df2 = DataFrame(
        {"foo": Series(["a", "b", "c"]).astype(cat_dtype), "right": [3, 2, 1]}
    ).set_index("foo")

    result = df1.merge(df2, left_index=True, right_index=True)

    expected = DataFrame(
        {"left": [1, 2], "right": [3, 2], "foo": Series(["a", "b"]).astype(cat_dtype)}
    ).set_index("foo")

    tm.assert_frame_equal(result, expected)

