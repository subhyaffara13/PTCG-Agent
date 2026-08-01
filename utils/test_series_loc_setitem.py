
def test_series_loc_setitem(indexer):
    df = DataFrame({"a": [1, 2, 3], "b": 1})

    with tm.raises_chained_assignment_error():
        df["a"].loc[indexer] = 0

