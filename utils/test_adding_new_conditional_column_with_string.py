
def test_adding_new_conditional_column_with_string(dtype, infer_string) -> None:
    # https://github.com/pandas-dev/pandas/issues/56204
    df = DataFrame({"a": [1, 2], "b": [3, 4]})
    with pd.option_context("future.infer_string", infer_string):
        df.loc[df["a"] == 1, "c"] = "1"
    expected = DataFrame({"a": [1, 2], "b": [3, 4], "c": ["1", float("nan")]}).astype(
        {"a": "int64", "b": "int64", "c": dtype}
    )
    tm.assert_frame_equal(df, expected)

