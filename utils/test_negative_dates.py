
def test_negative_dates():
    # https://github.com/pandas-dev/pandas/issues/50787
    ts = Timestamp("-2000-01-01")
    msg = (
        " not yet supported on Timestamps which are outside the range of "
        "Python's standard library. For now, please call the components you need "
        r"\(such as `.year` and `.month`\) and construct your string from there.$"
    )
    func = "^strftime"
    with pytest.raises(NotImplementedError, match=func + msg):
        ts.strftime("%Y")

    msg = (
        " not yet supported on Timestamps which "
        "are outside the range of Python's standard library. "
    )
    func = "^date"
    with pytest.raises(NotImplementedError, match=func + msg):
        ts.date()
    func = "^isocalendar"
    with pytest.raises(NotImplementedError, match=func + msg):
        ts.isocalendar()
    func = "^timetuple"
    with pytest.raises(NotImplementedError, match=func + msg):
        ts.timetuple()
    func = "^toordinal"
    with pytest.raises(NotImplementedError, match=func + msg):
        ts.toordinal()

