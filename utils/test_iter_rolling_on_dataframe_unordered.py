
def test_iter_rolling_on_dataframe_unordered():
    # GH 43386
    df = DataFrame({"a": ["x", "y", "x"], "b": [0, 1, 2]})
    results = list(df.groupby("a").rolling(2))
    expecteds = [df.iloc[idx, [1]] for idx in [[0], [0, 2], [1]]]
    for result, expected in zip(results, expecteds, strict=True):
        tm.assert_frame_equal(result, expected)

