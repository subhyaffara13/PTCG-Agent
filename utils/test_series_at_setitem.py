
def test_series_at_setitem():
    df = DataFrame({"a": [1, 2, 3], "b": 1})

    with tm.raises_chained_assignment_error():
        df["a"].at[0] = 0

