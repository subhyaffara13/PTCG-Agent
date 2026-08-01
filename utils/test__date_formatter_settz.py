
def test_DateFormatter_settz():
    time = mdates.date2num(datetime.datetime(2011, 1, 1, 0, 0,
                                             tzinfo=mdates.UTC))
    formatter = mdates.DateFormatter('%Y-%b-%d %H:%M')
    # Default UTC
    assert formatter(time) == '2011-Jan-01 00:00'

    # Set tzinfo
    formatter.set_tzinfo('Pacific/Kiritimati')
    assert formatter(time) == '2011-Jan-01 14:00'

