
def test_resample_single_group_std(unit):
    # GH 3849
    s = Series(
        [30.1, 31.6],
        index=[Timestamp("20070915 15:30:00"), Timestamp("20070915 15:40:00")],
    )
    s.index = s.index.as_unit(unit)
    expected = Series(
        [0.75], index=DatetimeIndex([Timestamp("20070915")], freq="D").as_unit(unit)
    )
    result = s.resample("D").apply(lambda x: np.std(x))
    tm.assert_series_equal(result, expected)

