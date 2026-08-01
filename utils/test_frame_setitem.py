
def test_frame_setitem() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    expr = pd.col("a") == 2

    result = df.copy()
    result[expr] = 100
    expected = pd.DataFrame({"a": [1, 100], "b": [3, 100]})
    tm.assert_frame_equal(result, expected)


def test_frame_setitem(indexer):
    df = DataFrame({"a": [1, 2, 3, 4, 5], "b": 1})

    with tm.raises_chained_assignment_error():
        df[0:3][indexer] = 10

