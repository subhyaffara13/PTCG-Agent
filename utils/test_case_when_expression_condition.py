
def test_case_when_expression_condition(df):
    # GH 64070
    result = df.assign(out=col("a").case_when([(col("a") > 1, 10), (col("a") <= 1, 5)]))
    expected = df.assign(out=Series([5, 10, 10], index=df.index))
    tm.assert_frame_equal(result, expected)

