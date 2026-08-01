
def test_bool_agg_dtype(op):
    # GH 7001
    # Bool sum aggregations result in int
    df = DataFrame({"a": [1, 1], "b": [False, True]})
    s = df.set_index("a")["b"]

    result = op(df.groupby("a"))["b"].dtype
    assert is_integer_dtype(result)

    result = op(s.groupby("a")).dtype
    assert is_integer_dtype(result)

