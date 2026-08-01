
def test_dictlike_lambda(ops, by_row, expected):
    # GH53601
    df = DataFrame({"a": [1, 2]})
    result = df.apply(ops, by_row=by_row)
    tm.assert_equal(result, expected)

