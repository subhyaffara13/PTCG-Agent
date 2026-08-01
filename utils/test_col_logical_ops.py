
def test_col_logical_ops(
    expr: Expression, expected_values: list[bool], expected_str: str
) -> None:
    # https://github.com/pandas-dev/pandas/issues/63322
    df = pd.DataFrame({"a": [True, False, True, False], "b": [False, True, True, True]})
    result = df.assign(c=expr)
    expected = pd.DataFrame(
        {
            "a": [True, False, True, False],
            "b": [False, True, True, True],
            "c": expected_values,
        }
    )
    tm.assert_frame_equal(result, expected)
    assert str(expr) == expected_str

    # Test that the expression works with .loc
    result = df.loc[expr]
    expected = df[expected_values]
    tm.assert_frame_equal(result, expected)

