
def test_frame_iloc_setitem(indexer):
    df = DataFrame({"a": [1, 2, 3, 4, 5], "b": 1})

    with tm.raises_chained_assignment_error():
        df[0:3].iloc[indexer] = 10

