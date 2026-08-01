
def test_rrulewrapper():
    def attach_tz(dt, zi):
        return dt.replace(tzinfo=zi)

    _test_rrulewrapper(attach_tz, dateutil.tz.gettz)

    SYD = dateutil.tz.gettz('Australia/Sydney')
    dtstart = datetime.datetime(2017, 4, 1, 0)
    dtend = datetime.datetime(2017, 4, 4, 0)
    rule = mdates.rrulewrapper(freq=dateutil.rrule.DAILY, dtstart=dtstart,
                               tzinfo=SYD, until=dtend)
    assert rule.after(dtstart) == datetime.datetime(2017, 4, 2, 0, 0,
                                                    tzinfo=SYD)
    assert rule.before(dtend) == datetime.datetime(2017, 4, 3, 0, 0,
                                                   tzinfo=SYD)

    # Test parts of __getattr__
    assert rule._base_tzinfo == SYD
    assert rule._interval == 1


def test_rrulewrapper():
    r = rrulewrapper(2)
    try:
        pickle.loads(pickle.dumps(r))
    except RecursionError:
        print('rrulewrapper pickling test failed')
        raise

