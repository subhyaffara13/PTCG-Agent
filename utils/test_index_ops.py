
def test_index_ops(func, request):
    idx, view_ = index_view([1, 2])
    expected = idx.copy(deep=True)
    if "astype" in request.node.callspec.id:
        expected = expected.astype("Int64")
    idx = func(idx)
    view_.iloc[0, 0] = 100
    tm.assert_index_equal(idx, expected, check_names=False)

