
def test_case_when_expression_math_condition_in_assign():
    # GH 64070
    df = DataFrame({"a": [-1, 1, 2], "b": [0, -2, 1]})
    caselist = [(col("a") + col("b") > 0, 99)]
    result = df.assign(flag=col("a").case_when(caselist=caselist))
    expected = df.assign(flag=Series([-1, 1, 99], index=df.index))
    tm.assert_frame_equal(result, expected)

