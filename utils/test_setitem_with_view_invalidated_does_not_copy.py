
def test_setitem_with_view_invalidated_does_not_copy(request):
    df = DataFrame({"a": [1, 2, 3], "b": 1, "c": 1})
    view = df[:]

    df["b"] = 100
    arr = get_array(df, "a")
    view = None  # noqa: F841
    # TODO(CoW) block gets split because of `df["b"] = 100`
    # which introduces additional refs, even when those of `view` go out of scopes
    df.iloc[0, 0] = 100
    # Setitem split the block. Since the old block shared data with view
    # all the new blocks are referencing view and each other. When view
    # goes out of scope, they don't share data with any other block,
    # so we should not trigger a copy
    mark = pytest.mark.xfail(reason="blk.delete does not track references correctly")
    request.applymarker(mark)
    assert np.shares_memory(arr, get_array(df, "a"))

