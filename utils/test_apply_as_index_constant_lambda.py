
def test_apply_as_index_constant_lambda(as_index, expected):
    # GH 13217
    df = DataFrame({"a": [1, 1, 2, 2], "b": [1, 1, 2, 2], "c": [1, 1, 1, 1]})
    result = df.groupby(["a", "b"], as_index=as_index).apply(lambda x: 1)
    tm.assert_equal(result, expected)

