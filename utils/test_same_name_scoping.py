
def test_same_name_scoping(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((20, 2)),
        index=date_range("20130101", periods=20, unit="ns"),
    )
    temp_hdfstore.put("df", df, format="table")
    expected = df[df.index > Timestamp("20130105")]

    result = temp_hdfstore.select("df", "index>datetime.datetime(2013,1,5)")
    tm.assert_frame_equal(result, expected)

    # changes what 'datetime' points to in the namespace where
    #  'select' does the lookup

    # technically an error, but allow it
    result = temp_hdfstore.select("df", "index>datetime.datetime(2013,1,5)")
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df", "index>datetime(2013,1,5)")
    tm.assert_frame_equal(result, expected)

