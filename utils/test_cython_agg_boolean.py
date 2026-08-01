
def test_cython_agg_boolean():
    frame = DataFrame(
        {
            "a": np.random.default_rng(2).integers(0, 5, 50),
            "b": np.random.default_rng(2).integers(0, 2, 50).astype("bool"),
        }
    )
    result = frame.groupby("a")["b"].mean()
    # GH#53425
    expected = frame.groupby("a")["b"].agg(np.mean)

    tm.assert_series_equal(result, expected)

