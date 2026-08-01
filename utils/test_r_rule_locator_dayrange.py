
def test_RRuleLocator_dayrange():
    loc = mdates.DayLocator()
    x1 = datetime.datetime(year=1, month=1, day=1, tzinfo=mdates.UTC)
    y1 = datetime.datetime(year=1, month=1, day=16, tzinfo=mdates.UTC)
    loc.tick_values(x1, y1)

