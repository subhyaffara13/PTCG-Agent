
def test_not_c_contiguous_mask(groupby_func):
    # https://github.com/pandas-dev/pandas/issues/61031
    if groupby_func == "corrwith":
        # corrwith is deprecated
        return
    df = DataFrame({"a": [1, 1, 2], "b": [3, 4, 5]}, dtype="Int64")
    reversed = DataFrame(
        {"a": [2, 1, 1], "b": [5, 4, 3]}, dtype="Int64", index=[2, 1, 0]
    )[::-1]
    assert not reversed["b"].array._mask.flags["C_CONTIGUOUS"]
    args = get_groupby_method_args(groupby_func, df)

    gb_reversed = reversed.groupby("a")
    result = getattr(gb_reversed, groupby_func)(*args)
    gb = df.groupby("a")
    expected = getattr(gb, groupby_func)(*args)
    tm.assert_equal(result, expected)

