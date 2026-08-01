
def test_inplace_ops(
    op: Callable, expected_values: list[object], expected_str: str
) -> None:
    # https://github.com/pandas-dev/pandas/pull/64267
    df = pd.DataFrame({"a": [1, 2]})
    expr = pd.col("a")
    expr = op(expr, 2)
    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2], "c": expected_values})
    tm.assert_frame_equal(result, expected)
    assert str(expr) == expected_str

