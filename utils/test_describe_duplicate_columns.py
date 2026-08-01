
def test_describe_duplicate_columns():
    # GH#50806
    df = DataFrame([[0, 1, 2, 3]])
    df.columns = [0, 1, 2, 0]
    gb = df.groupby(df[1])
    result = gb.describe(percentiles=[])

    columns = ["count", "mean", "std", "min", "max"]
    frames = [
        DataFrame([[1.0, val, np.nan, val, val]], index=[1], columns=columns)
        for val in (0.0, 2.0, 3.0)
    ]
    expected = pd.concat(frames, axis=1)
    expected.columns = MultiIndex(
        levels=[[0, 2], columns],
        codes=[5 * [0] + 5 * [1] + 5 * [0], 3 * list(range(5))],
    )
    expected.index.names = [1]
    tm.assert_frame_equal(result, expected)

