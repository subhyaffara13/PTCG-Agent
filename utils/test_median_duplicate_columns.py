
def test_median_duplicate_columns():
    # GH 14233

    df = DataFrame(
        np.random.default_rng(2).standard_normal((20, 3)),
        columns=list("aaa"),
        index=date_range("2012-01-01", periods=20, freq="s"),
    )
    result = df.resample("5s").median()
    df.columns = ["a", "b", "c"]
    expected = df.resample("5s").median()
    expected.columns = result.columns
    tm.assert_frame_equal(result, expected)

