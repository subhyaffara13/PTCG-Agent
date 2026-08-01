
def test_loc_with_mi_indexer():
    # https://github.com/pandas-dev/pandas/issues/35351
    df = DataFrame(
        data=[["a", 1], ["a", 0], ["b", 1], ["c", 2]],
        index=MultiIndex.from_tuples(
            [(0, 1), (1, 0), (1, 1), (1, 1)], names=["index", "date"]
        ),
        columns=["author", "price"],
    )
    idx = MultiIndex.from_tuples([(0, 1), (1, 1)], names=["index", "date"])
    result = df.loc[idx, :]
    expected = DataFrame(
        [["a", 1], ["b", 1], ["c", 2]],
        index=MultiIndex.from_tuples([(0, 1), (1, 1), (1, 1)], names=["index", "date"]),
        columns=["author", "price"],
    )
    tm.assert_frame_equal(result, expected)

