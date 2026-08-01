
def test_nanosecond_resample_error():
    # GH 12307 - Values falls after last bin when
    # Resampling using pd.tseries.offsets.Nano as period
    start = 1443707890427
    exp_start = 1443707890400
    indx = date_range(start=pd.to_datetime(start), periods=10, freq="100ns")
    ts = Series(range(len(indx)), index=indx)
    r = ts.resample(pd.tseries.offsets.Nano(100))
    result = r.agg("mean")

    exp_indx = date_range(start=pd.to_datetime(exp_start), periods=10, freq="100ns")
    exp = Series(range(len(exp_indx)), index=exp_indx, dtype=float)

    tm.assert_series_equal(result, exp)

