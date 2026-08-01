
def test_core_interval():
    for c in (Interval, Interval(0, 2)):
        check(c)

