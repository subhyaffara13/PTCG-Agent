
def test_nano_timepoint():
    time = datetime.datetime.now()
    time1 = m.test_nano_timepoint(time, datetime.timedelta(seconds=60))
    assert time1 == time + datetime.timedelta(seconds=60)

