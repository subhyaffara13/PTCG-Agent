
def test_to_datetime_wrapped_datetime64_ps():
    # GH#60341
    result = to_datetime([np.datetime64(1901901901901, "ps")])
    expected = DatetimeIndex(
        ["1970-01-01 00:00:01.901901901"], dtype="datetime64[ns]", freq=None
    )
    tm.assert_index_equal(result, expected)

