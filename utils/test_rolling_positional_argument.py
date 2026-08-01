
def test_rolling_positional_argument(grouping, _index, raw):
    # GH 34605

    def scaled_sum(*args):
        if len(args) < 2:
            raise ValueError("The function needs two arguments")
        array, scale = args
        return array.sum() / scale

    df = DataFrame(data={"X": range(5)}, index=[0, 0, 1, 1, 1])

    expected = DataFrame(data={"X": [0.0, 0.5, 1.0, 1.5, 2.0]}, index=_index)
    # GH 40341
    if "by" in grouping:
        expected = expected.drop(columns="X", errors="ignore")
    result = df.groupby(**grouping).rolling(1).apply(scaled_sum, raw=raw, args=(2,))
    tm.assert_frame_equal(result, expected)

