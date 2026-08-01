
def test_groupby_quantile_dt64tz_period():
    # GH#51373
    dti = pd.date_range("2016-01-01", periods=1000, unit="ns")
    df = pd.Series(dti).to_frame().copy()
    df[1] = dti.tz_localize("US/Pacific")
    df[2] = dti.to_period("D")
    df[3] = dti - dti[0]
    df.iloc[-1] = pd.NaT

    by = np.tile(np.arange(5), 200)
    gb = df.groupby(by)

    result = gb.quantile(0.5)

    # Check that we match the group-by-group result
    exp = {i: df.iloc[i::5].quantile(0.5) for i in range(5)}
    expected = DataFrame(exp).T.infer_objects()
    expected.index = expected.index.astype(int)

    tm.assert_frame_equal(result, expected)

