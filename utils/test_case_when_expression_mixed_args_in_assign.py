
def test_case_when_expression_mixed_args_in_assign():
    # GH 64070
    df = DataFrame({"name": ["Jason", "Amy", "Bob"], "age": [42, 10, 5]})
    caselist = [
        (lambda s: s < 10, col("age") + 100),
        (col("name").eq("Jason"), 1),
    ]
    result = df.assign(elderly=col("age").case_when(caselist=caselist))
    expected = df.assign(elderly=Series([1, 10, 105], index=df.index))
    tm.assert_frame_equal(result, expected)

