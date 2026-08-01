
def test_store_periodindex(temp_h5_path, format):
    # GH 7796
    # test of PeriodIndex in HDFStore
    df = DataFrame(
        np.random.default_rng(2).standard_normal((5, 1)),
        index=pd.period_range("20220101", freq="M", periods=5),
    )

    df.to_hdf(temp_h5_path, key="df", mode="w", format=format)
    expected = pd.read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df, expected)

