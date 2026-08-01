
def test_cython_agg_nothing_to_agg_with_dates():
    frame = DataFrame(
        {
            "a": np.random.default_rng(2).integers(0, 5, 50),
            "b": ["foo", "bar"] * 25,
            "dates": pd.date_range("now", periods=50, freq="min"),
        }
    )
    msg = "Cannot use numeric_only=True with SeriesGroupBy.mean and non-numeric dtypes"
    with pytest.raises(TypeError, match=msg):
        frame.groupby("b").dates.mean(numeric_only=True)

