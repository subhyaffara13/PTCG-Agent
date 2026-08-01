
def test_apply_noreduction_tzaware_object():
    # https://github.com/pandas-dev/pandas/issues/31505
    expected = DataFrame(
        {"foo": [Timestamp("2020", tz="UTC")]}, dtype="datetime64[ns, UTC]"
    )
    result = expected.apply(lambda x: x)
    tm.assert_frame_equal(result, expected)
    result = expected.apply(lambda x: x.copy())
    tm.assert_frame_equal(result, expected)

