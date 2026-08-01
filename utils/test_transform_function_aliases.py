
def test_transform_function_aliases(df):
    result = df.groupby("A").transform("mean", numeric_only=True)
    expected = df.groupby("A")[["C", "D"]].transform(np.mean)
    tm.assert_frame_equal(result, expected)

    result = df.groupby("A")["C"].transform("mean")
    expected = df.groupby("A")["C"].transform(np.mean)
    tm.assert_series_equal(result, expected)

