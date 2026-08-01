
def test_case_when_expression_missing_values_in_assign():
    # GH 64070
    df = DataFrame({"age": [np.nan, 5.0, 20.0]})
    caselist = [
        (col("age").isna(), "missing"),
        (col("age") > 10, "adult"),
    ]
    result = df.assign(group=col("age").case_when(caselist=caselist))
    expected = df.assign(
        group=Series(["missing", 5.0, "adult"], index=df.index, dtype=object)
    )
    tm.assert_frame_equal(result, expected)

