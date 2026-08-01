
def test_series_iloc_setitem(indexer):
    df = DataFrame({"a": [1, 2, 3], "b": 1})

    with tm.raises_chained_assignment_error():
        df["a"].iloc[indexer] = 0

