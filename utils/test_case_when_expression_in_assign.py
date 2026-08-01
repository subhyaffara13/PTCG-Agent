
def test_case_when_expression_in_assign():
    # GH 64070
    df = DataFrame({"age": [65, 30], "name": ["Jason", "Anna"]})
    result = df.assign(elderly=col("age").case_when([(col("name").eq("Jason"), 1)]))
    expected = df.assign(elderly=Series([1, 30], index=df.index))
    tm.assert_frame_equal(result, expected)

