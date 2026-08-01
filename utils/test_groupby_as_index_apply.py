
def test_groupby_as_index_apply(as_index):
    # GH #4648 and #3417
    df = DataFrame(
        {
            "item_id": ["b", "b", "a", "c", "a", "b"],
            "user_id": [1, 2, 1, 1, 3, 1],
            "time": range(6),
        }
    )
    gb = df.groupby("user_id", as_index=as_index)

    expected = DataFrame(
        {
            "item_id": ["b", "b", "a", "a"],
            "user_id": [1, 2, 1, 3],
            "time": [0, 1, 2, 4],
        },
        index=[0, 1, 2, 4],
    )
    result = gb.head(2)
    tm.assert_frame_equal(result, expected)

    # apply doesn't maintain the original ordering
    # changed in GH5610 as the as_index=False returns a MI here
    if as_index:
        tp = [(1, 0), (1, 2), (2, 1), (3, 4)]
        index = MultiIndex.from_tuples(tp, names=["user_id", None])
    else:
        index = Index([0, 2, 1, 4])
    expected = DataFrame(
        {
            "item_id": list("baba"),
            "time": [0, 2, 1, 4],
        },
        index=index,
    )
    result = gb.apply(lambda x: x.head(2))
    tm.assert_frame_equal(result, expected)

