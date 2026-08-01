
def test_series_iat_setitem():
    df = DataFrame({"a": [1, 2, 3], "b": 1})

    with tm.raises_chained_assignment_error():
        df["a"].iat[0] = 0

