
def test_store_timezone(temp_hdfstore):
    # GH2852
    # issue storing datetime.date with a timezone as it resets when read
    # back in a new timezone

    # original method
    today = date(2013, 9, 10)
    df = DataFrame([1, 2, 3], index=[today, today, today])
    temp_hdfstore["obj1"] = df
    result = temp_hdfstore["obj1"]
    tm.assert_frame_equal(result, df)

    # with tz setting
    with tm.set_timezone("EST5EDT"):
        today = date(2013, 9, 10)
        df = DataFrame([1, 2, 3], index=[today, today, today])
        temp_hdfstore["obj2"] = df

    with tm.set_timezone("CST6CDT"):
        result = temp_hdfstore["obj2"]

    tm.assert_frame_equal(result, df)

