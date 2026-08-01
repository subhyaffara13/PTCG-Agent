
def test_calendar_roundtrip_issue(temp_hdfstore):
    # 8591
    # doc example from tseries holiday section
    weekmask_egypt = "Sun Mon Tue Wed Thu"
    holidays = [
        "2012-05-01",
        dt.datetime(2013, 5, 1),
        np.datetime64("2014-05-01"),
    ]
    bday_egypt = pd.offsets.CustomBusinessDay(
        holidays=holidays, weekmask=weekmask_egypt
    )
    mydt = dt.datetime(2013, 4, 30)
    dts = date_range(mydt, periods=5, freq=bday_egypt)

    s = Series(dts.weekday, dts).map(Series("Mon Tue Wed Thu Fri Sat Sun".split()))

    temp_hdfstore.put("fixed", s)
    result = temp_hdfstore.select("fixed")
    tm.assert_series_equal(result, s)

    temp_hdfstore.append("table", s)
    result = temp_hdfstore.select("table")
    tm.assert_series_equal(result, s)

