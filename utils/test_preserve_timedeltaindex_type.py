
def test_preserve_timedeltaindex_type(temp_hdfstore, unit):
    # GH9635
    df = DataFrame(np.random.default_rng(2).normal(size=(10, 5)))
    df.index = timedelta_range(
        start="0s", periods=10, freq="1s", name="example", unit=unit
    )

    temp_hdfstore["df"] = df
    tm.assert_frame_equal(temp_hdfstore["df"], df)

