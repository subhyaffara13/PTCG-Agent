
def test_frame_loc() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    expr = pd.col("a") == 2
    result = df.copy()
    result.loc[expr, "b"] = 100
    expected = pd.DataFrame({"a": [1, 2], "b": [3, 100]})
    tm.assert_frame_equal(result, expected)

