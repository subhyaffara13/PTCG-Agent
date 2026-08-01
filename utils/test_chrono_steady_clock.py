
def test_chrono_steady_clock():
    time1 = m.test_chrono5()
    assert isinstance(time1, datetime.timedelta)

