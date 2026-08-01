
def test_drange():
    """
    This test should check if drange works as expected, and if all the
    rounding errors are fixed
    """
    start = datetime.datetime(2011, 1, 1, tzinfo=mdates.UTC)
    end = datetime.datetime(2011, 1, 2, tzinfo=mdates.UTC)
    delta = datetime.timedelta(hours=1)
    # We expect 24 values in drange(start, end, delta), because drange returns
    # dates from a half open interval [start, end)
    assert len(mdates.drange(start, end, delta)) == 24

    # Same if interval ends slightly earlier
    end = end - datetime.timedelta(microseconds=1)
    assert len(mdates.drange(start, end, delta)) == 24

    # if end is a little bit later, we expect the range to contain one element
    # more
    end = end + datetime.timedelta(microseconds=2)
    assert len(mdates.drange(start, end, delta)) == 25

    # reset end
    end = datetime.datetime(2011, 1, 2, tzinfo=mdates.UTC)

    # and tst drange with "complicated" floats:
    # 4 hours = 1/6 day, this is an "dangerous" float
    delta = datetime.timedelta(hours=4)
    daterange = mdates.drange(start, end, delta)
    assert len(daterange) == 6
    assert mdates.num2date(daterange[-1]) == (end - delta)

