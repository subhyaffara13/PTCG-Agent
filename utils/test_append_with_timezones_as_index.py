
def test_append_with_timezones_as_index(temp_hdfstore, gettz):
    # GH#4098 example

    dti = date_range("2000-1-1", periods=3, freq="h", tz=gettz("US/Eastern"))
    dti = dti._with_freq(None)  # freq doesn't round-trip

    df = DataFrame({"A": Series(range(3), index=dti)})

    temp_hdfstore.put("df", df)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

