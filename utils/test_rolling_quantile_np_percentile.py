
def test_rolling_quantile_np_percentile():
    # #9413: Tests that rolling window's quantile default behavior
    # is analogous to Numpy's percentile
    row = 10
    col = 5
    idx = date_range("20100101", periods=row, freq="B")
    df = DataFrame(
        np.random.default_rng(2).random(row * col).reshape((row, -1)), index=idx
    )

    df_quantile = df.quantile([0.25, 0.5, 0.75], axis=0)
    np_percentile = np.percentile(df, [25, 50, 75], axis=0)

    tm.assert_almost_equal(df_quantile.values, np.array(np_percentile))

