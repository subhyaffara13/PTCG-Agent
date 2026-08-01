
def test_case_when_expression_replacement(df):
    # GH 64070
    result = df.assign(
        out=col("a").case_when(
            [(df["a"] > 1, col("a") + 100), (df["a"] <= 1, col("a") + 1)]
        )
    )
    expected = df.assign(out=Series([2, 102, 103], index=df.index))
    tm.assert_frame_equal(result, expected)

