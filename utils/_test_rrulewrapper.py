
def _test_rrulewrapper(attach_tz, get_tz):
    SYD = get_tz('Australia/Sydney')

    dtstart = attach_tz(datetime.datetime(2017, 4, 1, 0), SYD)
    dtend = attach_tz(datetime.datetime(2017, 4, 4, 0), SYD)

    rule = mdates.rrulewrapper(freq=dateutil.rrule.DAILY, dtstart=dtstart)

    act = rule.between(dtstart, dtend)
    exp = [datetime.datetime(2017, 4, 1, 13, tzinfo=dateutil.tz.tzutc()),
           datetime.datetime(2017, 4, 2, 14, tzinfo=dateutil.tz.tzutc())]

    assert act == exp

