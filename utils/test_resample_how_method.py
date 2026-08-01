
def test_resample_how_method(unit):
    # GH9915
    s = Series(
        [11, 22],
        index=[
            Timestamp("2015-03-31 21:48:52.672000"),
            Timestamp("2015-03-31 21:49:52.739000"),
        ],
    )
    s.index = s.index.as_unit(unit)
    expected = Series(
        [11, np.nan, np.nan, np.nan, np.nan, np.nan, 22],
        index=DatetimeIndex(
            [
                Timestamp("2015-03-31 21:48:50"),
                Timestamp("2015-03-31 21:49:00"),
                Timestamp("2015-03-31 21:49:10"),
                Timestamp("2015-03-31 21:49:20"),
                Timestamp("2015-03-31 21:49:30"),
                Timestamp("2015-03-31 21:49:40"),
                Timestamp("2015-03-31 21:49:50"),
            ],
            freq="10s",
        ),
    )
    expected.index = expected.index.as_unit(unit)
    tm.assert_series_equal(s.resample("10s").mean(), expected)

