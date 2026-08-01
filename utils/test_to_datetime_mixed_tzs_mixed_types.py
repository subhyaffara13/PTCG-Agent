
def test_to_datetime_mixed_tzs_mixed_types():
    # GH#55793, GH#55693 mismatched tzs but one is str and other is
    #  datetime object
    ts = Timestamp("2016-01-02 03:04:05", tz="US/Pacific")
    dtstr = "2023-10-30 15:06+01"
    arr = [ts, dtstr]

    msg = (
        "Mixed timezones detected. Pass utc=True in to_datetime or tz='UTC' "
        "in DatetimeIndex to convert to a common timezone"
    )
    with pytest.raises(ValueError, match=msg):
        to_datetime(arr)
    with pytest.raises(ValueError, match=msg):
        to_datetime(arr, format="mixed")
    with pytest.raises(ValueError, match=msg):
        DatetimeIndex(arr)

