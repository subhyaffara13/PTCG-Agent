
def test_expression_getitem() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2, 3]})
    expr = pd.col("a")[1]
    expected_str = "col('a')[1]"

    assert str(expr) == expected_str

    result = df.assign(b=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [2, 2, 2]})
    tm.assert_frame_equal(result, expected)

