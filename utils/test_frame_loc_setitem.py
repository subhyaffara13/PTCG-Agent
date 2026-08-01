
def test_frame_loc_setitem(indexer):
    df = DataFrame({"a": [1, 2, 3, 4, 5], "b": 1})

    with tm.raises_chained_assignment_error():
        df[0:3].loc[indexer] = 10

