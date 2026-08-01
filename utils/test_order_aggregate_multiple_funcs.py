
def test_order_aggregate_multiple_funcs():
    # GH 25692
    df = DataFrame({"A": [1, 1, 2, 2], "B": [1, 2, 3, 4]})

    res = df.groupby("A").agg(["sum", "max", "mean", "ohlc", "min"])
    result = res.columns.levels[1]

    expected = Index(["sum", "max", "mean", "ohlc", "min"])

    tm.assert_index_equal(result, expected)

