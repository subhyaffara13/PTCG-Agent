
def test_frame_getitem() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    expr = pd.col("a") == 2
    result = df[expr]
    expected = df.iloc[[1]]
    tm.assert_frame_equal(result, expected)

