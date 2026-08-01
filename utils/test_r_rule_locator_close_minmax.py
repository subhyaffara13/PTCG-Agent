
def test_RRuleLocator_close_minmax():
    # if d1 and d2 are very close together, rrule cannot create
    # reasonable tick intervals; ensure that this is handled properly
    rrule = mdates.rrulewrapper(dateutil.rrule.SECONDLY, interval=5)
    loc = mdates.RRuleLocator(rrule)
    d1 = datetime.datetime(year=2020, month=1, day=1)
    d2 = datetime.datetime(year=2020, month=1, day=1, microsecond=1)
    expected = ['2020-01-01 00:00:00+00:00',
                '2020-01-01 00:00:00.000001+00:00']
    assert list(map(str, mdates.num2date(loc.tick_values(d1, d2)))) == expected

