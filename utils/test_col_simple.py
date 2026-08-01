
def test_col_simple(
    expr: Expression, expected_values: list[object], expected_str: str
) -> None:
    # https://github.com/pandas-dev/pandas/pull/64267
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": expected_values})
    tm.assert_frame_equal(result, expected)
    assert str(expr) == expected_str

