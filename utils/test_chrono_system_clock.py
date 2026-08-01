
def test_chrono_system_clock():
    # Get the time from both c++ and datetime
    date0 = datetime.datetime.today()
    date1 = m.test_chrono1()
    date2 = datetime.datetime.today()

    # The returned value should be a datetime
    assert isinstance(date1, datetime.datetime)

    # The numbers should vary by a very small amount (time it took to execute)
    diff_python = abs(date2 - date0)
    diff = abs(date1 - date2)

    # There should never be a days difference
    assert diff.days == 0

    # Since datetime.datetime.today() calls time.time(), and on some platforms
    # that has 1 second accuracy, we compare this way
    assert diff.seconds <= diff_python.seconds

