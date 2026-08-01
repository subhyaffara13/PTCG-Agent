
def test_resample_ohlc_result_odd_period(unit):
    # GH12348
    # raising on odd period
    rng = date_range("2013-12-30", "2014-01-07").as_unit(unit)
    index = rng.drop(
        [
            Timestamp("2014-01-01"),
            Timestamp("2013-12-31"),
            Timestamp("2014-01-04"),
            Timestamp("2014-01-05"),
        ]
    )
    df = DataFrame(data=np.arange(len(index)), index=index)
    result = df.resample("B").mean()
    expected = df.reindex(index=date_range(rng[0], rng[-1], freq="B").as_unit(unit))
    tm.assert_frame_equal(result, expected)

