
def test_date2num_dst_pandas(pd):
    # Test for github issue #3896, but in date2num around DST transitions
    # with a timezone-aware pandas date_range object.

    def tz_convert(*args):
        return pd.DatetimeIndex.tz_convert(*args).astype(object)

    _test_date2num_dst(pd.date_range, tz_convert)

